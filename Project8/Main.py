"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
import ntpath
from Parser import Parser
from CodeWriter import CodeWriter

flag = True

def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # Note: you can get the input file's name using:
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    parser = Parser(input_file)
    writer = CodeWriter(output_file)
    writer.set_file_name(input_filename)
    writer.writeinit()
    print("\n============")
    while parser.has_more_commands():
        line = parser.input_lines[parser.currLine]
        writeCommands(line, parser, writer)
        parser.advance()
    print("\n===========\nThe Translation has finished successfully")
    # writer.close()


def writeCommands(line, parser, writer):
    if parser.command_type(line) == "C_PUSH" or parser.command_type(line) == "C_POP":
        writer.write_push_pop(parser.command_type(line), parser.arg1(line), parser.arg2(line))
    elif parser.command_type(line) == "C_ARITHMETIC":
        writer.write_arithmetic(line)
    elif parser.command_type(line) == "C_LABEL":
        writer.writeLabel(parser.arg1(line))
    elif parser.command_type(line) == "C_GOTO":
        writer.writeGoto(parser.arg1(line))
    elif parser.command_type(line) == "C_IF":
        writer.writeIf(parser.arg1(line))
    elif parser.command_type(line) == "C_FUNCTION":
        writer.funcName = parser.arg1(line)
        writer.writeFunction(parser.arg1(line), parser.arg2(line))
    elif parser.command_type(line) == "C_CALL":
        writer.writeCall(parser.arg1(line), parser.arg2(line))
    elif parser.command_type(line) == "C_RETURN":
        writer.writeReturn()


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)
