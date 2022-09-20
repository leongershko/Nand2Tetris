"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import Dictionaries

i = 0


# segments = {"local": "LCL", "argument": "args", "pointer 0": "THIS",
#             "pointer 1": "THAT", "static": "static", "temp": "R5", "pointer": None}
# arithmetic1 = {"add": "M=M+D", "sub": "M=M-D", "and": "M=M&D", "or": "M=M|D", }
# arithmetic2 = {"gt": "JGT", "lt": "JLT", "eq": "JEQ", "neg": None, "not": None}

def TemplatePop(segment, index):
    if (segment in Dictionaries.segments):
        if segment == "static":
            index += 16
        elif segment == "temp":
            index += 5
        elif segment == "pointer":
            if index == 1:
                segment = "pointer 1"
                index = 4
            else:
                segment = "pointer 0"
                index = 3
            return "@SP\nAM=M-1\nD=M\n@{0}\nM=D\n".format(Dictionaries.segments[segment])
        return "@{0}\nD=M\n@{1}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M" \
               "\n@R13\nA=M\nM=D\n".format(Dictionaries.segments[segment], str(index))


def TemplatePush(segment, index):
    """
    Template for push Command
    :param segment: segment type
    :param index: input of index
    """
    push = None
    if "constant" in segment:
        push = "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str(index))
    elif segment in Dictionaries.segments:
        if segment == "static":
            index += 16
        elif segment == "temp":
            index += 5
        elif segment == "pointer":
            if index == 1:
                segment = "pointer 1"
            else:
                segment = "pointer 0"
            return "@{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(Dictionaries.segments[segment])
        push = "@{0}\nD=A\n@{1}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str(index),
                                                                                 Dictionaries.segments[segment])
    return push


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.file = output_stream
        self.currLine = 0
        self.order_number = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        print("the translation of VM file is started.")

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """

        template = ""

        if command in Dictionaries.arithmetic1:
            template = "@SP\nAM=M-1\nD=M\nA=A-1\n{0}\n".format(Dictionaries.arithmetic1[command])

        elif command in Dictionaries.arithmetic2:
            if command == "neg":
                template = "@SP\nA=M-1\nD=M\nM=-D\n"  # Check Later if doesnt work!!!!!
            elif command == "not":
                template = "@SP\nA=M-1\nM=!M\n"
            elif "shiftleft" in command:
                template = "@SP\nA=M-1\nM<<\n"
            elif "shiftright" in command:
                template = "@SP\nA=M-1\nM>>\n"
            elif command == "gt" or command == "lt":
                seg = Dictionaries.arithmetic2[command]
                template = "@SP\nAM=M-1\nD=M\n@CHECK{0}\nD;{1}\n@SP\n" \
                           "A=M-1\nD=M\n@X_POS{0}\nD;{1}\n(XY_POS{0})\n@SP\nA=M" \
                           "\nD=D-M\n@EQ{0}\nD;{2}\n(X_POS{0})\n@SP\nA=M-1\n" \
                           "M=-1\n@CONTINUE{0}\n0;JMP\n(EQ{0})\n@SP\nA=M-1\nM=0" \
                           "\n@CONTINUE{0}\n0;JMP\n(CHECK{0})\n@SP\nA=M-1\n" \
                           "D=M\n@XY_POS{0}\nD;{3}\n@SP\nA=M-1\nM=0\n(CONTINUE{0})\n" \
                    .format(str(self.order_number), seg[0], seg[1], seg[2])

            else:
                template = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{0}\n" \
                           "D;{1}\n@SP\nA=M-1\nM=0\n@CONTINUE{0}\n0;JMP\n" \
                           "(TRUE{0})\n@SP\nA=M-1\nM=-1\n(CONTINUE{0})" \
                           "\n".format(str(self.order_number), Dictionaries.arithmetic2[command])

            self.order_number += 1

        self.file.write(template)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        global i
        write_command = ""
        if command == "C_PUSH":
            write_command = TemplatePush(segment, index)
        elif command == "C_POP":
            write_command = TemplatePop(segment, index)

        self.file.write(write_command)

    def close(self) -> None:
        """Closes the output file."""
        self.file.close()

#              template = "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE{0}\n" \
#                            "D;{1}\n@SP\nA=M-1\nM=0\n@CONTINUE{0}\n0;JMP\n" \
#                            "(FALSE{0})\n@SP\nA=M-1\nM=-1\n(CONTINUE{0})" \
#                            "\n".format(str(self.order_number), Dictionaries.arithmetic2[command])
