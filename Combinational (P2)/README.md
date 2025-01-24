# Project 2: Boolean Arithmetic

## Overview

This project builds upon the logic gates from Project 1 to create chips capable of performing arithmetic operations. We implement a series of adders culminating in the Arithmetic Logic Unit (ALU), a key component of the CPU.

## Implementation Details

### Adder Chips

We implement a hierarchy of adder chips:

- HalfAdder: Adds two bits
- FullAdder: Adds three bits
- Add16: Adds two 16-bit numbers

### Arithmetic Logic Unit (ALU)

The ALU implementation:

- Performs arithmetic and logical operations
- Handles 16-bit inputs
- Produces 16-bit output and status flags
- Controlled by six control bits

### Incrementation

The Inc16 chip:

- Adds 1 to a 16-bit number
- Utilized in program counter implementation

## Architecture Design

The chips are organized in increasing complexity:

1. Basic addition (HalfAdder)
2. Carry handling (FullAdder)
3. Multi-bit operations (Add16)
4. Complex arithmetic/logic (ALU)

## Testing

Each chip includes:

- Test scripts (.tst)
- Compare files (.cmp)
- Output files (.out)

Testing procedure:

1. Implement each chip starting with HalfAdder
2. Test thoroughly before moving to more complex chips
3. Use the Hardware Simulator for verification

## Files Structure

```
project2/
│
├── HalfAdder.hdl      # 2-bit adder
├── FullAdder.hdl      # 3-bit adder
├── Add16.hdl          # 16-bit adder
├── Inc16.hdl          # 16-bit incrementer
└── ALU.hdl            # Arithmetic Logic Unit
```

## Learning Outcomes

This project teaches:

- Binary arithmetic implementation
- Carry propagation handling
- ALU design principles
- Multi-bit chip construction
- Efficient hardware arithmetic

## Implementation Notes

### ALU Functionality

The ALU supports:

- Basic arithmetic operations (addition, negation)
- Bitwise operations (AND)
- Output flag generation (zero, negative)
- Input preprocessing (zeroing, negation)

## Common Challenges and Solutions

1. Carry Chain Implementation

   - Solution: Careful consideration of carry propagation
   - Systematic testing with edge cases

2. ALU Control Logic

   - Truth table-based implementation
   - Systematic control bit handling
   - Thorough testing of all operations

3. Zero and Negative Detection
   - Efficient implementation of status flags
   - Handling edge cases correctly

## Next Steps

These arithmetic chips form the foundation for:

- Project 3's sequential chips
- The CPU's arithmetic capabilities
- Understanding computer architecture
