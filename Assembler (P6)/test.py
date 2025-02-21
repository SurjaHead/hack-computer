#!/usr/bin/env python3

import modal
import pyaudio
import wave
import io
import time
import numpy as np
from datetime import datetime
import threading
from queue import Queue
import paho.mqtt.client as mqtt
import sys
import os
import audioop
import scipy.signal as signal
from scipy.io import wavfile
from scipy.signal import resample_poly

# Set up Modal image with required dependencies
image = (
    modal.Image.debian_slim()
    .apt_install(["ffmpeg", "portaudio19-dev", "python3-dev", "libasound-dev"])
    .pip_install(["openai-whisper", "ffmpeg-python", "pyaudio", "numpy", "paho-mqtt", "scipy"])
)
app = modal.App("live-whisper-transcription", image=image)

# Set up cache directory for Whisper model
CACHE_DIR = "/cache"
cache_vol = modal.Volume.from_name("whisper-cache", create_if_missing=True)

# MQTT Configuration
MQTT_BROKER_ADDRESS = "localhost"
MQTT_TOPIC = "robot/drive"

# Audio Configuration
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 3
THRESHOLD = 500
DEVICE_RATE = 44100
TARGET_RATE = 16000
GAIN = 2.0

@app.cls(
    gpu=modal.gpu.T4(),
    volumes={CACHE_DIR: cache_vol},
    container_idle_timeout=60 * 10,
)
class WhisperModel:
    @modal.enter()
    def setup(self):
        import whisper
        print("Loading Whisper model...")
        self.model = whisper.load_model("large-v3-turbo", device="cuda", download_root=CACHE_DIR)
        print("Whisper model loaded successfully!")

    @modal.method()
    def transcribe(self, audio_data):
        try:
            print("Starting transcription...")
            # Save audio data to a temporary file
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data)
            
            result = self.model.transcribe("temp_audio.wav")
            print(f"Transcription result: {result['text']}")
            return result["text"]
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

class RobotController:
    def __init__(self):
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            self.client.connect(MQTT_BROKER_ADDRESS)
            self.client.loop_start()
            print("MQTT client connected successfully")
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            raise

    def move(self, direction):
        """Send movement commands via MQTT"""
        command_mapping = {
            "forward": "forward",
            "backward": "back",
            "left": "left",
            "right": "right"
        }
        
        if direction in command_mapping:
            command = command_mapping[direction]
            print(f"Sending command: {command}")
            try:
                self.client.publish(MQTT_TOPIC, command)
                time.sleep(1.0)
                self.client.publish(MQTT_TOPIC, "stop")
            except Exception as e:
                print(f"Error sending command: {e}")

    def cleanup(self):
        """Clean up MQTT connection"""
        try:
            self.client.publish(MQTT_TOPIC, "stop")
            self.client.loop_stop()
            self.client.disconnect()
            print("Robot controller shutdown complete")
        except Exception as e:
            print(f"Error during cleanup: {e}")

def preprocess_audio(audio_data, sample_rate):
    try:
        audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32767.0
        
        # Apply gain with limiter
        audio *= GAIN
        audio = np.clip(audio, -1.0, 1.0)
        
        # Resample properly
        if sample_rate != TARGET_RATE:
            audio = resample_poly(audio, TARGET_RATE, sample_rate)
        
        # RMS normalization
        rms = np.sqrt(np.mean(audio**2))
        if rms > 0.001:  # Avoid division by zero
            target_rms = 0.05  # Adjust this value
            audio *= (target_rms / rms)
        
        # Dither and convert to int16
        dither = np.random.randn(len(audio)) * 0.003  # White noise dither
        audio = np.clip(audio + dither, -1.0, 1.0)
        audio = (audio * 32767).astype(np.int16)
        
        buffer = io.BytesIO()
        wavfile.write(buffer, TARGET_RATE, audio)
        return buffer.getvalue()
    except Exception as e:
        print(f"Error preprocessing audio: {e}")
        return None

def process_command(text):
    """Extract movement commands from text"""
    text = text.lower().strip()
    command_phrases = {
        "forward": ["forward", "go forward", "move forward", "ahead", "straight", "forwards", 
                   "front", "go front", "move ahead", "straight ahead"],
        "backward": ["backward", "back", "go back", "move back", "reverse", "backwards", 
                    "behind", "go behind", "reverse back"],
        "left": ["left", "turn left", "go left", "move left", "take left"],
        "right": ["right", "turn right", "go right", "move right", "take right"]
    }
    
    # First try exact matches
    words = text.split()
    for command, phrases in command_phrases.items():
        if any(word in phrases for word in words):
            return command
            
    # Then try partial matches
    for command, phrases in command_phrases.items():
        if any(phrase in text for phrase in phrases):
            return command
            
    return None

def record_audio_stream(audio_queue, stop_event):
    """Continuously record audio and add to queue"""
    try:
        p = pyaudio.PyAudio()
        
        # Get default device info
        default_device = None
        print("\nAvailable Input Devices:")
        for i in range(p.get_device_count()):
            try:
                dev_info = p.get_device_info_by_index(i)
                if dev_info.get('maxInputChannels') > 0:
                    print(f"Device {i}: {dev_info.get('name')}")
                    # Prefer USB devices or devices with "mic" in the name
                    if default_device is None or \
                       'usb' in dev_info.get('name').lower() or \
                       'mic' in dev_info.get('name').lower():
                        default_device = i
                        print(f"Selected device {i} as default")
            except:
                continue

        if default_device is None:
            raise Exception("No input devices found!")

        print(f"\nUsing device {default_device}")
        
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=DEVICE_RATE,
                       input=True,
                       input_device_index=default_device,
                       frames_per_buffer=CHUNK)

        print("* Recording started")
        print("Speak commands clearly: forward, backward, left, right")
        print("Audio level indicator: ", end='', flush=True)

        while not stop_event.is_set():
            frames = []
            has_significant_audio = False
            max_level = 0
            
            # Record audio
            for _ in range(0, int(DEVICE_RATE / CHUNK * RECORD_SECONDS)):
                if stop_event.is_set():
                    break
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    
                    # Calculate audio level
                    rms = audioop.rms(data, 2)
                    level = min(50, int(rms / 100))
                    max_level = max(max_level, rms)
                    print(f"\rAudio level: {'|' * level}{' ' * (50-level)} {rms:5d}", end='', flush=True)
                    
                    if rms > THRESHOLD:
                        has_significant_audio = True
                        
                except Exception as e:
                    print(f"\nAudio recording error: {e}")
                    continue
            
            if has_significant_audio:
                try:
                    print(f"\nProcessing audio (max level: {max_level})")
                    
                    # Combine all audio frames
                    audio_data = b''.join(frames)
                    
                    # Preprocess audio
                    processed_audio = preprocess_audio(audio_data, DEVICE_RATE)
                    if processed_audio:
                        audio_queue.put(processed_audio)
                    
                except Exception as e:
                    print(f"\nError processing audio: {e}")
            else:
                print("\rListening...", end='', flush=True)

    except Exception as e:
        print(f"Error in audio stream: {e}")
    finally:
        try:
            stream.stop_stream()
            stream.close()
            p.terminate()
        except:
            pass
        print("\n* Recording stopped")

@app.local_entrypoint()
def main():
    print("Initializing transcription service...")
    try:
        model = WhisperModel()
        robot = RobotController()
        
        audio_queue = Queue()
        stop_event = threading.Event()
        last_command = None
        last_command_time = 0
        
        record_thread = threading.Thread(
            target=record_audio_stream, 
            args=(audio_queue, stop_event)
        )
        record_thread.start()
        
        print("\nStarting continuous transcription... (Press Ctrl+C to stop)")
        print("Speak clearly and a bit louder than normal")
        
        while True:
            if not audio_queue.empty():
                try:
                    audio_data = audio_queue.get()
                    transcription = model.transcribe.remote(audio_data)
                    
                    # Clean up transcription
                    cleaned_text = transcription.lower().strip()
                    
                    # Skip if transcription is just noise or empty
                    if cleaned_text in ["you", "", "the", "a", "um", "uh"] or len(cleaned_text) < 2:
                        continue
                    
                    command = process_command(cleaned_text)
                    current_time = time.time()
                    
                    if command and (command != last_command or current_time - last_command_time > 1.5):
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"\n[{timestamp}] Command detected: {command}")
                        print(f"Full transcription: {cleaned_text}")
                        robot.move(command)
                        last_command = command
                        last_command_time = current_time
                    else:
                        print(f"\rTranscribed: {cleaned_text}", end='', flush=True)
                except Exception as e:
                    print(f"\nError processing audio: {e}")
                    continue
                    
    except KeyboardInterrupt:
        print("\nStopping transcription service...")
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        stop_event.set()
        record_thread.join()
        robot.cleanup()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()