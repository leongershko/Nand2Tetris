"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


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
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        self.currLine = 0
        # f = open(input_file, "r")
        self.input_lines = remove_com_space(input_file)
        self.length = len(self.input_lines)

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """

        return not (self.length == self.currLine)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self.currLine += 1

    def command_type(self) -> str:
        """
        ****if it comes to this func then we know it isnt white space or Comment****
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if (self.input_lines[self.currLine][0] == '@'):
            return "A_COMMAND"
        elif (self.input_lines[self.currLine][0] == "("):
            return "L_COMMAND"

        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
            else Return None
        """
        if (self.command_type() == "A_COMMAND"):
            return self.input_lines[self.currLine][1::]
        elif (self.command_type() == "L_COMMAND"):
            return self.input_lines[self.currLine][1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.command_type() == "C_COMMAND":
            # return self.input_lines[self.currLine][0]
            if "=" in self.input_lines[self.currLine]:
                ind = self.input_lines[self.currLine].find('=')
                return self.input_lines[self.currLine][:ind]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.command_type() == "C_COMMAND":
            if "=" in self.input_lines[self.currLine]:
                ind = self.input_lines[self.currLine].find('=')
                return self.input_lines[self.currLine][ind + 1::]

            if ";" in self.input_lines[self.currLine]:
                ind = self.input_lines[self.currLine].find(';')
                ind_e = self.input_lines[self.currLine].find(';')
                return self.input_lines[self.currLine][:ind]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """

        # Your code goes here!
        if self.command_type() == "C_COMMAND":
            if ";" in self.input_lines[self.currLine]:
                ind = self.input_lines[self.currLine].find(';')
                return self.input_lines[self.currLine][ind + 1::]

# a = Parser("assemb.txt")
# print(a.input_lines)
# while(a.has_more_commands()):
#     print(a.comp(), "Comp")
#     print(a.dest(), "dest")
#     print(a.symbol(), "Symbol")
#     print(a.jump(), "jump")
#
#     a.advance()
