# Project 1: Boolean Logic

## Overview

This project implements fundamental logic gates that form the building blocks of our computer system. Starting with a NAND gate as our primitive operation, we construct a complete family of logic gates.

## Implementation Details

### Basic Gates

We implement the following basic logic gates:

- Not: Negation of input
- And: Logical AND operation
- Or: Logical OR operation
- Xor: Exclusive OR operation

### Multi-Way Variants

Extended implementations include:

- 16-bit variants of basic gates
- Multi-way gates (Or8Way)
- Multiplexers (Mux, Mux4Way16, Mux8Way16)
- Demultiplexers (DMux, DMux4Way, DMux8Way)

## Testing

Each gate includes corresponding test files:

- Individual test scripts (.tst)
- Compare files (.cmp) for verification
- Output files (.out) generated during testing

To test the implementation:

1. Load the .tst file in the Hardware Simulator
2. Run the script
3. Compare output with the .cmp file

## Files Structure

```
project1/
│
├── And.hdl            # And gate implementation
├── And16.hdl          # 16-bit And gate
├── DMux.hdl           # Demultiplexer
├── DMux4Way.hdl       # 4-way demultiplexer
├── DMux8Way.hdl       # 8-way demultiplexer
├── Mux.hdl            # Multiplexer
├── Mux16.hdl          # 16-bit multiplexer
├── Mux4Way16.hdl      # 4-way 16-bit multiplexer
├── Mux8Way16.hdl      # 8-way 16-bit multiplexer
├── Not.hdl            # Not gate
├── Not16.hdl          # 16-bit Not
├── Or.hdl             # Or gate
├── Or16.hdl           # 16-bit Or
├── Or8Way.hdl         # 8-way Or
└── Xor.hdl            # Xor gate
```

## Learning Outcomes

Through this project, we gain understanding of:

- Boolean algebra and logic design
- Hardware Description Language (HDL)
- Gate-level implementation strategies
- Hardware simulation and testing

## Common Challenges and Solutions

1. Understanding HDL Syntax

   - Solution: Careful study of the HDL specification
   - Practice with simple gates before complex ones

2. Efficient NAND Usage

   - Focus on minimizing gate count
   - Balance between efficiency and readability

3. Multi-Way Gate Design
   - Systematic approach to complex gates
   - Reuse of simpler components

## Next Steps

The gates implemented here serve as foundation for Project 2, where we'll build arithmetic chips using these basic logic gates.
