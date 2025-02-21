# Projects 7 & 8: VM Translator

## Overview

The VM Translator is a crucial component that bridges the gap between high-level programming and assembly code. It translates stack-based VM commands into Hack assembly language, implementing a two-tier compilation process similar to Java's bytecode compilation.

## Implementation Details

### Project 7 Components

The basic VM translator implements:

- Stack arithmetic operations
- Memory access commands
- Push/pop operations for various segments

### Project 8 Extensions

The complete VM translator adds:

- Program flow commands (goto, if-goto)
- Function calling commands
- Function return handling
- Multi-file program support
- Bootstrap code generation

## Architecture

### Key Components

1. Parser

   - Reads VM commands
   - Handles command classification
   - Extracts command components

2. Code Writer

   - Generates assembly code
   - Manages symbol table
   - Handles memory segments

3. Main Program
   - Coordinates translation process
   - Manages file I/O
   - Implements command-line interface

## Memory Segment Mapping

Implements standard mapping for:

- Local: LCL
- Argument: ARG
- This: THIS
- That: THAT
- Pointer: 3-4
- Temp: 5-12
- Static: 16-255

## Testing Programs

### Project 7 Tests

- SimpleAdd
- StackTest
- BasicTest
- PointerTest
- StaticTest

### Project 8 Tests

- BasicLoop
- FibonacciSeries
- SimpleFunction
- NestedCall
- FibonacciElement
- StaticsTest

## Files Structure

```
vm_translator/
│
├── src/
│   ├── parser.py          # Command parsing
│   ├── code_writer.py     # Assembly generation
│   ├── main.py           # Main program
│   └── constants.py      # Shared constants
│
├── tests/
│   ├── basic_tests/      # Project 7 tests
│   └── function_tests/   # Project 8 tests
│
└── examples/
    └── sample_programs/  # Example VM programs
```

## Usage Instructions

### Basic Usage

```bash
python vm_translator.py <input_path>
```

### Options

- Single file translation
- Directory translation

## Learning Outcomes

This project provides understanding of:

- Stack-based virtual machines
- Two-tier compilation
- Assembly code generation
- Memory management
- Function call mechanics
