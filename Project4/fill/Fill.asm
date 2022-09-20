// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//declareVal
@SCREEN
D=M
@start
M=0
@8192 //EndScreen - StartScreen
D=A
@flag
M=D

(INIT)
@SCREEN //Finished
D=M
@start
M=0
@CHECK
0;JMP //GoBackToCheck

(CHECK)
@KBD
D=M
@BLACK
D;JNE
@WHITE
D;JEQ


(WHITE) // ElseWhite
@flag
D=M
@start
D=D-M
@INIT
D;JEQ 

@start
D=M
@SCREEN
A=A+D
M=0 //MakeWhite
@start
M=M+1 //increseVal
@WHITE
0;JMP

(BLACK)
@flag
D=M
@start
D=D-M
@INIT
D;JEQ 

@start
D=M
@SCREEN
A=A+D
M=-1 //MakeBlack
@start
M=M+1 //increseVal
@BLACK
0;JMP

(INIT)
@start
M=0
@CHECK
0;JMP 

