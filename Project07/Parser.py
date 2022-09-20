"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

segments = {"local": "LCL", "argument": "args", "pointer 0": "THIS",
            "pointer 1": "THAT", "static": "static", "temp": "R5", "pointer": None}
arithmetic1 = {"add": "M=M+D", "sub": "M=M-D", "and": "M=M&D", "or": "M=M|D", }
arithmetic2 = {"gt": "JGT", "lt": "JLT", "eq": "JEQ", "neg": None, "not": None}
import typing

import Dictionaries


# Functions
def remove_com_space(f):
    inp_lines_as_list = [line.rstrip('\n') for line in f]
    input_lines_no_space = [line.replace(' ', "") for line in inp_lines_as_list]

    new_lst = input_lines_no_space.copy()
    for i, val in enumerate(input_lines_no_space):
        if val[:2] == "//":
            new_lst[i] = ""

        elif "//" in val:
            ind = val.find("//")
            new_val = val[:ind]
            new_lst[i] = new_val
    # Remove the new lines in the Array
    new_lst = [val for val in new_lst if val != ""]

    return new_lst


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # self.file = input_file Open input file
        self.currLine = 0
        self.input_lines = remove_com_space(input_file)
        self.length = len(self.input_lines)

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return not (self.length == self.currLine)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        if self.has_more_commands():
            self.currLine += 1

    def command_type(self, string) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        if "push" in string:
            return "C_PUSH"
        elif "pop" in string:
            return "C_POP"
        elif string in Dictionaries.arithmetic1 or string in Dictionaries.arithmetic2:
            return "C_ARITHMETIC"

    def arg1(self, string) -> str:
        """
        Returns: Segment
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        c_type = self.command_type(string)
        ind = len(string) - 1
        while not string[ind].isalpha():
            ind = ind - 1

        if c_type == "C_PUSH":
            return string[4:ind + 1]
        if c_type == "C_POP":
            return string[3:ind + 1]
        # return c_type

    def arg2(self, string) -> int:
        """
        Returns: Index
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        c_type = self.command_type(string)
        ind = len(string) - 1
        while not string[ind].isalpha():
            ind = ind - 1

        if (c_type == "C_PUSH"):
            return int(string[ind + 1:])
        elif c_type == "C_POP":
            return int(string[ind + 1:])

