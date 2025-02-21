# Projects 10 & 11: Jack Compiler

## Overview

A two-stage Jack compiler implementation that translates Jack programming language into VM code executable on the Hack platform. Project 10 implements syntax analysis (parsing), while Project 11 extends this with code generation.

## Architecture

### Project 10: Syntax Analysis

- **JackTokenizer**: Performs lexical analysis
- **CompilationEngine**: Conducts syntax analysis
- **SymbolTable**: Manages variable scoping and properties
- **XML Output**: Generates structured representation of program syntax

### Project 11: Code Generation

- **VMWriter**: Generates VM commands
- **Expression Handling**: Translates complex expressions to VM operations
- **Control Flow**: Implements if/while/return statements
- **Object Management**: Handles method calls and object instantiation

## Implementation Details

### File Structure

```
compiler/
│
├── src/
│   ├── JackTokenizer.py       # Lexical analysis
│   ├── CompilationEngine.py   # Parsing and code generation
│   ├── SymbolTable.py         # Symbol management
│   ├── VMWriter.py            # VM code generation
│   └── JackCompiler.py        # Main program
│
├── tests/
│   ├── ExpressionlessSquare/  # Basic syntax testing
│   ├── Square/                # Complete syntax testing
│   ├── ArrayTest/             # Array handling test
│   │
│   ├── Seven/                 # Basic expression test
│   ├── ConvertToBin/          # Control flow test
│   ├── Average/               # Array manipulation test
│   ├── Pong/                  # Complete application
│   └── ComplexArrays/         # Advanced array operations
└── docs/
    └── implementation_notes.md # Design decisions and algorithms
```

### Key Components

#### JackTokenizer

- Removes comments and whitespace
- Classifies tokens (keyword, symbol, identifier, integer, string)
- Provides sequential token access
- Handles language-specific lexical details

#### CompilationEngine

- Implements recursive descent parsing
- Validates syntax against Jack grammar
- Manages nested language constructs
- Generates code in code generation phase

#### SymbolTable

- Maintains class and subroutine scopes
- Tracks variable types, kinds, and indices
- Handles variable declaration and access
- Manages static/field/local/argument variables

#### VMWriter

- Generates arithmetic commands
- Implements memory segment access
- Handles function declarations and calls
- Manages control flow statements

## Language Features Implemented

### Syntax Analysis (Project 10)

- Class structure and declarations
- Method, constructor, and function definitions
- Variable declarations
- Statements (let, if, while, do, return)
- Expressions and operators
- Array access
- Method calls

### Code Generation (Project 11)

- Stack-based arithmetic and logic
- Variable allocation and access
- Object instantiation and method dispatch
- Array creation and indexing
- Control structures
- Function call mechanism

## Usage Instructions

### Syntax Analysis Mode

```bash
python JackAnalyzer.py <input_file_or_directory>
```

Generates XML files representing the program structure.

### Full Compilation Mode

```bash
python JackCompiler.py <input_file_or_directory>
```

Generates .vm files executable on the VM Emulator.

## Verification Process

1. **Syntax Analysis Verification**:

   - Compare generated XML with reference files
   - Validate structure correctness
   - Verify token classification

2. **Code Generation Verification**:
   - Execute generated VM code
   - Test program functionality
   - Verify against expected behavior
   - Validate memory usage patterns

## Technical Implementation Notes

### Memory Segment Mapping

- `static` → static segment
- `field` → this segment
- `local` → local segment
- `argument` → argument segment

### Object Handling

- Constructor: Allocates memory, initializes object
- Method: Implicitly passes `this`
- Function: Static subroutine

### Array Implementation

- Array.new: Memory allocation
- Array indexing: Pointer arithmetic
- Array assignment: Memory segment manipulation
