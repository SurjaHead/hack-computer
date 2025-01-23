// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

@R1
D=M          // D = R1
@i
M=D          // i = R1

@0
D=0
@R2
M=D          // R2 = 0 (initialize result)

@R0
D=M          // D = R0 (multiplicand)
@LOOP
0;JMP        // Jump to LOOP

(LOOP)
@R0
D=M    
@R2
M=D+M        // R2 = R2 + R0

@i
M=M-1        // i = i - 1
D=M          // D = i
@END
D;JEQ        // If D == 0, jump to END

@LOOP
0;JMP        // Jump back to LOOP

(END)
// End of multiplication
