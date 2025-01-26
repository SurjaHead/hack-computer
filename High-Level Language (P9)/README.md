# Project 9: Pong Game Implementation

## Overview

A classic Pong game implementation using the Jack programming language. This project demonstrates object-oriented programming concepts through a fully interactive game that features real-time graphics, keyboard input handling, and collision detection.

## Game Structure

### File Organization

```
High-Level Language (P9)/
│
├── Main.jack          # Program entry point and game initialization
├── PongGame.jack      # Game state management and main game loop
├── Ball.jack          # Ball movement and collision physics
├── Paddle.jack        # Paddle control and movement logic
└── README.md         # Implementation documentation
```

### Class Descriptions

#### Main.jack

- Entry point for the game
- Initializes the PongGame instance
- Manages program lifecycle

#### PongGame.jack

- Orchestrates game components
- Manages game state and scoring
- Handles game loop and updates
- Coordinates interactions between ball and paddle

#### Ball.jack

- Manages ball position and velocity
- Implements ball movement physics
- Handles wall and paddle collisions
- Controls ball speed and direction

#### Paddle.jack

- Implements paddle movement
- Handles keyboard input for paddle control
- Manages paddle position constraints
- Controls paddle size and properties

## Technical Implementation

### Graphics System

- Screen buffer management for smooth animation
- Real-time rendering of game objects
- Efficient screen updates for performance
- Collision boundary visualization

### Input Handling

- Real-time keyboard monitoring
- Paddle movement control
- Game state controls (restart, quit)
- Response time optimization

## Building and Running

1. Compile the Jack files using the Jack compiler in the NAND2Tetris IDE.

2. Run in VM Emulator:

- Load the compiled Pong directory
- Adjust speed slider as needed
- Click "Run" to start the game

## Game Controls

- Left Arrow: Move right paddle up
- Right Arrow: Move right paddle down
- W: Move left paddle up
- S: Move left paddle down
- Q: Quit game

## Implementation Features

### Core Game Mechanics

- Smooth paddle movement
- Realistic ball physics
- Score tracking
- Wall and paddle collisions

## Known Limitations

- At the moment, both paddles cannot be moved at the same time, as the OS can't detect 2 keys pressed at the same time.

## Dependencies

- Jack OS API
  - Screen class for graphics
  - Keyboard class for input
  - Memory class for object management
- Jack Compiler
- VM Emulator

## Learning Outcomes

This implementation demonstrates:

- Object-oriented design in Jack
- Real-time game programming
- Graphics and animation techniques
- User input handling
- Game physics implementation
- Memory management in Jack
