<!-- # Hack Computer

---

This is a programmable 16-bit computer I built during the NAND2Tetris course. It was a result of my desire to understand to uncover the abstraction of computers.

**NOTE: I didn't realize that I could build new chips with previous chips I've built so most of my implementations in P1 are very convoluted, as I built them with NAND gates.**

## Content

- Project 1: Built elementary logic gates and chips

- Project 2: Built combinational chips along with the ALU

- Project 3: Build a register, RAM, and a program counter

- Project 4: Learned hack assembly by writing 2 programs:

  - Mult.asm: multiplies two numbers from R0 and R1 and displays the product in R2
  - Fill.asm: fills the screen with black whenever a key is pressed

- Project 5: Built the CPU, data memory, and instruction memory and put them together to build the computer

- Project 6: Built an assembler to convert hack assembly to machine language

---

I combined these to create a programmable computer that can perform any instructed task. You can test the computer in the [NAND2Tetris Online IDE](https://nand2tetris.github.io/web-ide/chip/).

In addition, I built an assembler in Python to convert Hack assembly (the language used to program this computer) into machine language.

You can test the asssembler by running main.py and providing the input and output file directories.

Here's an example of how it works:

Add.asm (adds the constants 2 and 3 and puts the sum in register 0):

```
// Computes R0 = 2 + 3  (R0 refers to RAM[0])

@2
D=A
@3
D=D+A
@0
M=D
```

Resulting Add.hack:

```
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000
``` -->

# Hack Computer

This repository contains my implementation of the projects from the "NAND2Tetris" course, where we build a modern 16-bit computer system from the ground up, starting with basic NAND gates and working our way up to high-level applications.

## Project Structure

The repository is organized into individual project folders, each focusing on a specific layer of the computer system:

### Hardware Projects (Projects 1-5)

- **Project 1**: Boolean Logic
  - Implementation of basic logic gates using NAND
  - Gates include Not, And, Or, Xor, Multiplexer, and Demultiplexer
- **Project 2**: Boolean Arithmetic
  - Implementation of arithmetic chips
  - Half-Adder, Full-Adder, ALU, and more
- **Project 3**: Sequential Logic
  - Implementation of memory elements
  - Flip-Flops, Registers, RAM units, and Program Counter
- **Project 4**: Machine Language Programming
  - Writing low-level assembly programs
  - Understanding the Hack machine language
- **Project 5**: Computer Architecture
  - Implementation of the Hack CPU and complete computer system
  - Integration of CPU, Memory, and I/O

### Software Projects (Projects 6-12)

- **Project 6**: Assembler
  - Translates assembly language into binary code
  - Written in [your chosen language]
- **Project 7-8**: VM Translator
  - Two-tier compilation implementation
  - Translates VM code into assembly
  - Handles stack arithmetic and memory access
- **Project 9**: High-Level Programming
  - Application development in Jack language
  - [Description of your specific implementation]
- **Project 10-11**: Compiler
  - Jack language compiler development
  - Syntax analysis and code generation
- **Project 12**: Operating System
  - Implementation of basic OS services
  - Math, Memory, Screen, Keyboard handling

## Technical Details

### Tools and Languages Used

- Hardware Description Language (HDL) for hardware simulation
- Python for software components such as the VM transalator and compiler
- Jack programming language for high-level applications

### Testing Methodology

To test the files, go to the [NAND2Tetris IDE](https://nand2tetris.github.io/web-ide/chip/), and choose the appropriate project. When you run the code, the IDE compares it to the answer and show's the different between the ideal output and your output.

## Getting Started

To explore this repository:

1. Clone the repository:

   ```bash
   git clone https://github.com/SurjaHead/hack-computer.git
   ```

2. Each project folder contains:

   - Source code files
   - Test files
   - README with project-specific details
   - Implementation notes where relevant

3. To run the projects:
   - Follow the setup instructions in each project's README
   - Use the official nand2tetris software suite available at www.nand2tetris.org

## Resources and References

- Official course website: www.nand2tetris.org
- Course textbook: "The Elements of Computing Systems"

## Acknowledgments

- Noam Nisan and Shimon Schocken for creating this amazing course

---

**Note**: This is an ongoing project, and some sections may be under development.
