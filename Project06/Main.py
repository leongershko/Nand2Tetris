"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import cmath
import math
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code

Shifts = {"A>>":1, "A<<":2, "D<<":3, "D>>":4, "M<<":5, "M>>":6 }

def into_binary(num):
    return ('{0:016b}'.format(num))

def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # *Initialization*
    # Initialize the symbol table with all the predefined symbols and their
    # pre-allocated RAM addresses, according to section 6.2.3 of the book.

    parser = Parser(input_file)
    sTable = SymbolTable()
    coder = Code()

    sTable.table = {"KBD": 24576, "SCREEN": 16384, "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4}
    for i in range(16):
        sTable.table["R" + str(i)] = i

    # FirstPass
    i = 0
    while (parser.has_more_commands()):
        if parser.command_type() == "L_COMMAND":
            if not sTable.contains(parser.symbol()):
                sTable.add_entry(parser.symbol(), i)
        else:
            i += 1

        parser.advance()

    # SecondPass
    parser.currLine = 0
    index_a = 16
    binary_code = "0000000000000000"
    while (parser.has_more_commands()):
        if parser.input_lines[parser.currLine] == "":
            parser.advance()
            continue

        if parser.command_type() == "A_COMMAND":
            if parser.symbol().isnumeric():
                output_file.write((into_binary(int(parser.symbol()))) + "\n")
                parser.advance()
                continue
            else:
                if sTable.contains(parser.symbol()):
                    output_file.write((into_binary(sTable.get_address(parser.symbol()))) + "\n")
                    parser.advance()
                    continue
                else:
                    sTable.add_entry(parser.symbol(), index_a)
                    index_a += 1
                    output_file.write((into_binary(sTable.get_address(parser.symbol()))) + "\n")

                    parser.advance()
                    continue

        if parser.command_type() == "C_COMMAND":
            if parser.comp() in Shifts:
                binary_code = "101"
            else:
                binary_code = "111"
            # ;
            if ";" in parser.input_lines[parser.currLine]:
                binary_code += coder.comp(parser.comp())
                binary_code += coder.dest("null")
                binary_code += coder.jump(parser.jump())
                output_file.write(binary_code + "\n")
            else:
                # =
                binary_code += coder.comp(parser.comp())
                binary_code += coder.dest(parser.dest())
                binary_code += coder.jump(parser.jump())
                output_file.write(binary_code + "\n")

        parser.advance()
# with open("assemb.txt", 'r') as input_file, \
#     open("output.txt", 'w') as output_file:
#     assemble_file(input_file, output_file)

# assemble_file("assemb.txt", "output.txt")

if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
