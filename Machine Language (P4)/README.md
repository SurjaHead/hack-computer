# Project 4: Machine Language Programming

## Overview

This project introduces machine language programming using the Hack assembly language. It bridges the gap between hardware and software, teaching fundamental concepts of low-level programming and computer architecture through hands-on experience with assembly code.

## Machine Language Fundamentals

### Hack Assembly Language

The Hack computer's assembly language includes:

- A-instructions: Address instructions (@value)
- C-instructions: Computation instructions (dest=comp;jump)
- Labels: Symbolic references to program locations
- Comments: Documentation within the code

### Memory Segments

Understanding and utilizing:

- RAM[0-15]: Virtual registers
- RAM[16-255]: Static variables
- RAM[256-2047]: Stack
- RAM[2048-16383]: Heap
- RAM[16384-24575]: Memory mapped I/O

## Programming Tasks

### Multiplication Program

Implementation of multiplication through repeated addition:

- Uses loops for iteration
- Manages memory locations
- Implements error checking
- Optimizes for efficiency

### I/O Handling Program

Screen and keyboard interaction:

- Screen memory mapping
- Keyboard input processing
- Real-time response
- Visual feedback

## File Structure

```
project4/
│
├── mult/
│   ├── Mult.asm           # Multiplication program
│   └── Mult.tst           # Test script
│
├── fill/
│   ├── Fill.asm           # Screen interaction program
│   └── Fill.tst           # Test script
│
└── examples/
    ├── Add.asm            # Addition example
    ├── Max.asm            # Maximum value example
    └── Rect.asm           # Rectangle drawing example
```

## Running Programs

1. Load program in CPU Emulator
2. Set up test conditions
3. Execute step-by-step or continuously
4. Verify results
