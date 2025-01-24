# Project 3: Sequential Logic

## Overview

This project introduces time-dependent components into our computer architecture, marking the transition from combinational to sequential logic. We build memory elements starting from a basic flip-flop and progressing to more complex memory units, culminating in Random Access Memory (RAM) implementations.

## Theoretical Foundation

Sequential logic differs fundamentally from the combinational logic we've worked with previously because it introduces the concept of state - the ability to remember values over time. This capability forms the foundation of computer memory and enables the creation of registers and counters essential for CPU operation.

## Implementation Details

### Data Flip-Flop (DFF)

The project begins with the DFF as our fundamental sequential building block. While we use it as a primitive, understanding its behavior is crucial:

- Outputs previous input on each clock cycle
- Forms the basis for all memory components
- Enables synchronized circuit behavior

### Basic Memory Elements

We implement several essential memory components:

1. Bit Register

   - Stores a single bit
   - Implements load functionality
   - Built using a DFF and multiplexer

2. Register

   - Stores a 16-bit value
   - Uses multiple bit registers in parallel
   - Forms the basis for larger memory units

3. RAM Units
   - RAM8: 8-register memory
   - RAM64: 64-register memory
   - RAM512: 512-register memory
   - RAM4K: 4096-register memory
   - RAM16K: 16384-register memory

### Program Counter

The program counter (PC) implementation:

- Maintains and increments instruction address
- Supports load and reset operations
- Crucial for program execution control

## File Structure

```
project3/
│
├── sequential/
│   ├── Bit.hdl              # Single-bit register
│   ├── Register.hdl         # 16-bit register
│   ├── PC.hdl              # Program counter
│   └── README.md           # Component documentation
│
├── memory/
│   ├── RAM8.hdl            # 8-register memory
│   ├── RAM64.hdl           # 64-register memory
│   ├── RAM512.hdl          # 512-register memory
│   ├── RAM4K.hdl           # 4K-register memory
│   └── RAM16K.hdl          # 16K-register memory
│
└── tests/
    ├── Bit.tst             # Bit tests
    ├── Register.tst        # Register tests
    └── RAM*.tst            # RAM unit tests
```

## Implementation Strategy

### Memory Hierarchy

The implementation follows a hierarchical approach:

1. Build basic storage elements (Bit, Register)
2. Construct small RAM units (RAM8)
3. Use smaller units to build larger ones
4. Implement addressing logic for each level

### Test Scripts

The project includes comprehensive test scripts:

- Built-in test files (.tst)
- Compare files (.cmp)
- Output files (.out)

## Learning Outcomes

Through this project, we gain understanding of:

- Sequential logic principles
- Memory hierarchy design
- Computer timing concepts
- Hardware verification methods
- Scalable hardware design

## Testing Individual Components

1. Load component into Hardware Simulator
2. Run corresponding test script
3. Verify against compare files
4. Debug if necessary
