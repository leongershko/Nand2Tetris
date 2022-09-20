"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

import Dictionaries


# Functions
def remove_com_space(f):
    new_backslash = [line.rstrip('\n') for line in f]
    inp_lines_as_list = [line.replace('\t', "") for line in new_backslash]

    new_lst = inp_lines_as_list.copy()
    for i, val in enumerate(inp_lines_as_list):
        # if val[:2] == "//":
        #     new_lst[i] = ""

        if "/" in val:
            ind = val.find("/")
            new_val = val[:ind]
            new_lst[i] = new_val

    # Remove the new lines in the Array
    new_lst = [val for val in new_lst if val != ""]
    lst = new_lst.copy()

    # Remove spaces at the end of the string
    for i,line in enumerate(new_lst):
        ind = len(line) - 1
        if line[ind] == " ":
            ind = ind - 1
            while line[ind] == " ":
                ind = ind - 1
        new_lst[i] = line[:ind+1]

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
        elif "label" in string:
            return "C_LABEL"
        elif "if" in string:
            return "C_IF"
        elif "goto" in string:
            return "C_GOTO"
        elif "function" in string:
            return "C_FUNCTION"
        elif "call" in string:
            return "C_CALL"
        elif "return" in string:
            return "C_RETURN"
        elif "shift" in string:
            return "C_ARITHMETIC"

    def arg1(self, string) -> str:
        """
        Returns: Segment
            str: the first argument of the current command. In case of
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
            Should not be called if the current command is "C_RETURN".
        """

        c_type = self.command_type(string)
        ind = len(string) - 1
        if string[ind] == " ":
            ind = ind - 1
            while string[ind] == " ":
                ind = ind - 1
        end = ind + 1

        while not string[ind] == " ":
            ind = ind - 1

        if c_type == "C_PUSH":
            return string[5:ind]
        if c_type == "C_POP":
            return string[4:ind]
        if c_type == "C_IF":
            return string[8:end]
        if c_type == "C_GOTO":
            return string[5:]
        if c_type == "C_FUNCTION":
            return string[9:ind]
        if c_type == "C_CALL":
            return string[5:ind]
        if c_type == "C_LABEL":
            return string[6:end]
        # if c_type == "SHIFT":
        #     return


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

        if string[ind] == " ":
            ind = ind - 1
            while string[ind] == " ":
                ind = ind - 1
        end = ind + 1
        while not string[ind] == " ":
            ind = ind - 1

        if (c_type == "C_PUSH"):
            return int(string[ind + 1:end])
        elif c_type == "C_POP":
            return int(string[ind + 1:end])
        elif c_type == "C_FUNCTION":
            return int(string[ind + 1:end])
        elif c_type == "C_CALL":
            return int(string[ind + 1:end])

