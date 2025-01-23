# Hack Computer

---

This is a programmable 16-bit computer I built during the NAND2Tetris course. It was a result of my desire to understand to uncover the abstraction of computers.

*** NOTE: I didn't realize that I could build new chips with previous chips I've built so most of my implementations in P1 are very convoluted, as I built them with NAND gates.

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
```
