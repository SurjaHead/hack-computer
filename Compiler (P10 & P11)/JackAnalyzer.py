import os
import sys
from VMCompilationEngine import CompilationEngine

def main():
    # Get the path to the file or directory
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Enter the path to the Jack file or directory: ").strip()

    try:
        # Check if the path exists
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist")
            return

        # Check if the path is a directory
        if os.path.isdir(path):
            # Get a list of all the .jack files in the directory
            jack_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".jack")]
            
            if not jack_files:
                print(f"Error: No .jack files found in '{path}'")
                return
                
            print(f"Found {len(jack_files)} Jack files in '{path}'")
            
            # Iterate over each file and compile it
            for file in jack_files:
                output_file = file.replace(".jack", ".vm")
                print(f"Compiling {os.path.basename(file)} to {os.path.basename(output_file)}...")
                try:
                    CompilationEngine(file, output_file)
                    print(f"Successfully compiled {os.path.basename(file)}")
                except Exception as e:
                    print(f"Error compiling {os.path.basename(file)}: {str(e)}")
        
        elif path.endswith(".jack"):
            # Compile the single file
            output_file = path.replace(".jack", ".vm")
            print(f"Compiling {os.path.basename(path)} to {os.path.basename(output_file)}...")
            try:
                CompilationEngine(path, output_file)
                print(f"Successfully compiled {os.path.basename(path)}")
            except Exception as e:
                print(f"Error compiling {os.path.basename(path)}: {str(e)}")
        else:
            print(f"Error: '{path}' is not a Jack file or directory")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
if __name__ == "__main__":
    main()