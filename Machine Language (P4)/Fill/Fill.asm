// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Define the memory address for the keyboard input
@KBD      // Address of the keyboard memory-mapped register
D=M       // Load the value of KBD into D register

(INFINITE_LOOP) // Label for the infinite loop
    @KBD        // Re-read the keyboard input
    D=M         // Store the keyboard input value in D register
    
    @PRESSED
    M=D // stores the kbd value

    @ISKEYPRESSED
    D;JNE // if kbd is pressed, it goes to the function iskeypressed

 (CONTINUE)
    @PREVSTATE
    D=M

    @PRESSED
    D=D-M

    @CHANGE
    D;JNE // if there is a state change, it goes to the change function

    @KBD
    D=M

    @NOINPUT // If no key is pressed (D=0), continue looping
    D;JEQ       // Jump to the loop to turn the pixels white when there's no input
    // Logic of what to do with keyboard input
    @SCREEN
    D=A // storing screen address in D

    @NEWPIXEL
    M=D // storing screen address in a variable NEWPIXEL

    @COUNTER
    D=M // storing counter's value in D

    @NEWPIXEL
    M=D+M // adding the counter's value to the screen address
    
    @NEWPIXEL
    A=M   // using the value in NEWPIXEL as an address to manipulate
    M=-1 // setting the value at NEWPIXEL address to -1 (sets 16 pixels to 0, compared to 1, which just sets one pixel)
    
    @COUNTER
    M=M+1 // updating counter by 1 to iterate through the pixels
    
    @PREVSTATE
    M=1
    @INFINITE_LOOP // Go back to continuously check for new input
    0;JMP

//function to change kbd input to a boolean value
(ISKEYPRESSED)
@PRESSED
M=1 // sets pressed to 1 if kbd is pressed
D=0
@CONTINUE
D;JEQ // goes back to the continue checkpoint

//function to reset counter
(CHANGE)
@COUNTER
M=0 // resets counter if prevstate and current state are different
@PRESSED
D=M
@PREVSTATE
M=D // sets prevstate to current state
@INFINITE_LOOP
0;JMP // goes back to the beginning of the loop


(NOINPUT)
    @PRESSED
    M=0
    @SCREEN
    D=A

    @NEWPIXEL
    M=D

    @COUNTER
    D=M

    @NEWPIXEL
    M=D+M
    
    @NEWPIXEL
    A=M
    M=0 // same logic as above, but setting to 0 here to clear the pixels
    
    @COUNTER
    M=M+1
    
    @PREVSTATE
    M=0
    @INFINITE_LOOP
    0;JMP










