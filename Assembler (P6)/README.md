# Project 6: Assembler

## Overview

The assembler marks our transition from hardware to software development, bridging the gap between human-readable assembly code and machine-executable binary instructions. This project implements a two-pass assembler that translates programs written in the Hack assembly language into binary code that can execute on the Hack computer platform we built in Project 5.

## Assembler Architecture

### Two-Pass Implementation

Our assembler operates in two distinct passes through the source code:

First Pass:

- Builds the symbol table
- Processes label declarations (xxx)
- Handles predefined symbols
- Assigns addresses to variables

Second Pass:

- Generates binary code
- Resolves symbolic references
- Handles variable allocation
- Produces final machine code

### Symbol Management

The symbol table handles several types of symbols:

1. Predefined Symbols:

   - Virtual registers (R0-R15)
   - Special memory locations (SCREEN, KBD)
   - Special purposes (SP, LCL, ARG, THIS, THAT)

2. Label Symbols:

   - User-defined labels in parentheses (LOOP)
   - Mapped to instruction addresses
   - Used for program flow control

3. Variable Symbols:
   - User-defined variables
   - Allocated from RAM[16] onward
   - Managed during assembly

## Implementation Details

### File Structure

```
assembler/
│
├── src/
│   ├── main.py           # Main program
│   ├── parser.py         # Assembly code parser
│   ├── code.py           # Binary code generator
│   ├── symboltable.py    # Symbol management
│   └── utils.py          # Helper functions
│
├── tests/
│   ├── add/              # Basic arithmetic tests
│   ├── max/              # Branching and loops
│   └── pong/             # Complex program test
│
└── examples/
    ├── Rect.asm          # Rectangle drawing
    └── Pong.asm          # Pong game source
```

### Key Components

1. Parser Module:

   - Removes comments and whitespace
   - Identifies instruction types
   - Extracts instruction components
   - Handles symbolic references

2. Code Generator:

   - Converts A-instructions
   - Translates C-instructions
   - Generates binary output
   - Ensures correct formatting

3. Symbol Table:
   - Manages symbol mappings
   - Handles address allocation
   - Provides efficient lookup
   - Maintains scope rules

## Instruction Processing

### A-Instructions

Handling @value instructions:

- Numeric values converted directly
- Symbolic references resolved
- Variables allocated as needed
- 15-bit address generation

### C-Instructions

Processing dest=comp;jump:

- Comp field binary encoding
- Dest field translation
- Jump condition handling
- 16-bit instruction formation

## Testing Strategy

### Unit Testing

Component-level verification:

1. Parser Testing:

   - Instruction recognition
   - Symbol extraction
   - Comment handling
   - Error detection

2. Code Generator Testing:

   - Binary conversion accuracy
   - Instruction formatting
   - Edge case handling
   - Output validation

3. Symbol Table Testing:
   - Symbol addition
   - Address allocation
   - Lookup functionality
   - Scope management

### Integration Testing

End-to-end program assembly:

- Basic arithmetic programs
- Control flow programs
- Complex applications
- Error handling verification

## Usage Instructions

### Command Line Interface

```bash
python assembler.py input.asm [output.hack]
```

Options:

- Input file (required): Assembly source
- Output file (optional): Binary output
- Debug mode flag
- Verbose output option

## Learning Outcomes

This project teaches:

- Assembly language processing
- Symbol table management
- Binary code generation
- File format handling
- Error management
