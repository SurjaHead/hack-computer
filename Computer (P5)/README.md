# Project 5: Computer Architecture

## Overview

This project represents the culmination of our hardware construction journey, where we integrate all previously built components into a complete von Neumann computer architecture. The Hack computer we build demonstrates fundamental principles of modern computer architecture while maintaining enough simplicity to be fully comprehensible.

## Architectural Components

### Central Processing Unit (CPU)

The CPU serves as the heart of our computer system, integrating several key components we built in previous projects:

- The Arithmetic Logic Unit (ALU) from Project 2 handles all computations
- Registers from Project 3 store and manage data
- The Program Counter guides program execution
- Control logic orchestrates all operations according to the current instruction

Our CPU implementation supports the complete Hack instruction set while maintaining a clean and efficient design. The control logic decodes instructions and manages data flow between components, demonstrating the elegant simplicity of the Harvard architecture.

### Memory System

The memory architecture encompasses several distinct areas:

- Data Memory (RAM) for variable storage and runtime data
- Instruction Memory (ROM) containing the program instructions
- Memory-Mapped I/O for screen and keyboard interaction

The memory system implementation showcases the practical application of the RAM units we developed in Project 3, now integrated into a cohesive system with proper addressing and data management.

### Computer Integration

The complete computer integrates the CPU and memory components into a functional system:

- Clean interfaces between components
- Synchronized operations via the system clock
- Proper reset handling
- Efficient instruction execution cycle

## Implementation Details

### File Structure

```
project5/
│
├── CPU/
│   ├── CPU.hdl           # Central Processing Unit implementation
│   ├── CPU.tst           # CPU test scripts
│   └── CPU-external.tst  # External CPU tests
│
├── Memory/
│   ├── Memory.hdl        # Memory system implementation
│   └── Memory.tst        # Memory tests
│
├── Computer/
│   ├── Computer.hdl      # Complete computer implementation
│   └── ComputerRect.tst  # Rectangle program test
│
└── programs/
    ├── Rect.hack         # Rectangle drawing program
    └── Pong.hack         # Pong game program
```

### Component Interfaces

The CPU interface includes:

```vhdl
IN  inM[16],         // M value input  (M = contents of RAM[A])
    instruction[16],  // Instruction for execution
    reset;           // Signals whether to restart the current program
OUT outM[16],        // M value output
    writeM,          // Write to M?
    addressM[15],    // Address in data memory (of M)
    pc[15];          // Address of next instruction
```

The Memory interface demonstrates:

```vhdl
IN  in[16],      // Data input
    load,        // Write enable
    address[15]; // Address location
OUT out[16];     // Data output
```

### Test Programs

We use several programs to verify system functionality:

1. Rectangle Program:

   - Draws a rectangle on the screen
   - Tests basic computation and I/O
   - Verifies program flow control

2. Pong Game:
   - Complex interactive program
   - Tests all system aspects
   - Demonstrates real-world capability

<!-- ## Implementation Notes

### CPU Design Decisions

The CPU implementation reflects several key design choices:

1. Instruction Handling:

   - Efficient instruction decoding
   - Optimized control signal generation
   - Clean separation of A and C instructions

2. Data Path Organization:

   - Direct paths for common operations
   - Minimized propagation delays
   - Efficient register usage

3. Control Logic:
   - Straightforward instruction decoding
   - Clear control signal generation
   - Predictable timing behavior

### Memory Organization

The memory system demonstrates careful consideration of:

1. Address Space Management:

   - Clean separation of segments
   - Efficient address decoding
   - Fast access to all regions

2. I/O Handling:
   - Seamless screen integration
   - Responsive keyboard input
   - Efficient memory mapping
 -->

## Learning Outcomes

This project provides deep understanding of:

- Computer architecture principles
- Hardware-software interaction
- System integration techniques
- Digital design methodology
- Testing and verification approaches

## Running Programs

To execute programs on the computer:

1. Load the Computer.hdl implementation
2. Choose a program file (.hack)
3. Use the hardware simulator
4. Monitor execution results
