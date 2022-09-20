// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

// Put your code here.

@R14
D=M
@i //LOCATION
M=D // initialize i to the beginning of the array
@counter
M=0

@j 
M=0
// vars for Swap function
@result
M=0
@var1
M=0
@var2
M=0

(CHECK)// array.length - i > 0 
@counter
D=M
@R15
D=M-D
D=D-1
@END // 
D;JEQ
// else go to inner loop
@LOOP
0;JMP


(LOOP)
// length - i - 1 > 0
@R14
D=M
@i
D = M-D
@R15
D=M-D
D=D-1
@ENDIN
D;JEQ

//arr[i]
@i
A=M
D=M
@var1
M=D
@result
M=D

//arr[i+1]
@i
M=M+1
A=M
D=M
@var2
M=D
@result
D=M-D //arr[i]-arr[i+1] = var1-var2
@SWAP
D;JLT

@CHECK
0;JMP



(SWAP)
@var1
D=M
@i //arr[i+1]
A=M
M=D //arr[i+1] = var1
@i
M=M-1
@var2
D=M
@i
A=M // arr[i]
M=D //arr[i] = var2
@i // i+1
M=M+1
@j
M=M+1
@LOOP
0;JMP

(ENDIN) // End of inner loop, nullify j, and add one to i
@0
D=A
@j
M=D
@R14
D=M
@i //LOCATION
M=D 
@counter
M=M+1
@CHECK
0;JMP

(END)
@END
0;JMP
