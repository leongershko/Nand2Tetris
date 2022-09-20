"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import Dictionaries

i = 0


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.
        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.file = output_stream
        self.order_number = 0
        self.funcName = ""
        self.inp_file = ""
        self.filename = None

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.
        Args:
            filename (str): The name of the VM file.
        """
        self.filename = filename
        print("the translation of " + filename + " file is started.")

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
            if "neg" in command:
                template = "@SP\nA=M-1\nD=M\nM=-D\n"
            elif "not" in command:
                template = "@SP\nA=M-1\nM=!M\n"
            elif "shiftleft" in command:
                template = "@SP\nAM=M-1\nM<<\n@SP\nM=M+1\n"
            elif "shiftright" in command:
                template = "@SP\nAM=M-1\nM>>\n@SP\nM=M+1\n"
            elif "gt" in command or "lt" in command:
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

        self.file.write("//Arethmetic : " + command + "\n")
        self.file.write(template)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        write_command = "//Write Push||Pop\n"
        if command == "C_PUSH":
            write_command = "//Push Command\n" + self.TemplatePush(segment, index)
        elif command == "C_POP":
            write_command = "//Pop Command\n" + self.TemplatePop(segment, index)

        self.file.write(write_command)

    def close(self) -> None:
        """Closes the output file."""
        self.file.close()

    def writeinit(self):
        """
        Writes the assembly code that effects the
        VM initialization (also called bootstrap
        code). This code should be placed in the
        ROM beginning in address 0x0000.
        Returns: none

        """
        write_command = "@256\nD=A\n@SP\nM=D\n"
        self.file.write(write_command)
        self.writeCall("Sys.init", '0')

    def writeLabel(self, label) -> None:
        """
        Writes the assembly code that is the
        translation of the given label command.
        Args:
            label:
        Returns: writes (label)

        """
        write_command = "(" + self.funcName + "$" + str(label) + ".)\n"
        self.file.write(write_command)

    def writeGoto(self, goto) -> None:
        """
        Writes the assembly code that is the
        translation of the given goto command.
        Args:
            string:

        Returns:

        """
        write_command = "@" + self.funcName + "$" + str(goto) + ".\n0;JMP\n"
        self.file.write(write_command)

    def writeIf(self, label) -> None:
        """
        Writes the assembly code that is the
        translation of the given if-goto command.
        Args:
            string:

        Returns:

        """
        write_command = "//writeIf\n@SP\nAM=M-1\nD=M\nA=A-1\n@" + self.funcName + "$" + str(label) +"." + "\nD;JNE\n"
        self.file.write(write_command)

    def writeFunction(self, functionName, numLocals) -> None:
        """
        Writes the assembly code that is the translation of
        the given Function command
        Args:
            numLocals:
        Returns:
        """
        write_command = "//writeFunc\n(" + self.funcName + ")\n"
        for i in range(int(numLocals)):
            write_command += "@SP\nA=M\n\nM=0\n@SP\nM=M+1\n"
        self.file.write(write_command)


    def writeReturn(self) -> None:
        """
        Writes the assembly code that is the
    translation of the given Call command.
        Args:
            functionName:
            numArgs:

        Returns: None
        """
        write_command = "@LCL\nD=M\n@endFrame" + str(Dictionaries.ret_count) + "\nM=D\n" \
                                                                               "@5\nD=D-A\nA=D\nD=M\n@returnAdd" + str(
            Dictionaries.ret_count) + "\nM=D\n" \
                                      "@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n" \
                                      "@ARG\nD=M\nD=D+1\n@SP\nM=D\n"

        k = 4
        for j in range(1, 5):
            write_command += "//EndFramesForReturn\n@endFrame" + str(Dictionaries.ret_count) + "\nD=M\n@" + str(
                j) + "\n" \
                     "A=D-A\nD=M\n@R" + str(k) + "\nM=D\n"
            k -= 1

        write_command += "@returnAdd" + str(Dictionaries.ret_count) + "\nA=M\n0;JMP\n"
        Dictionaries.ret_count += 1

        self.file.write(write_command)

    def writeCall(self, func_name, nargs) -> None:
        """
        Writes the assembly code that is the
        translation of the given Return command.
        Returns:

        """
        returnAdd = self.funcName + "$ret." + str(Dictionaries.ret_count)
        write_command = "//WriteCall \n@" + returnAdd + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n//Restores Segments\n"

        for arg in Dictionaries.helper_loop:
            write_command += "@" + arg + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        write_command += "//Set ARGS\n@5\nD=A\n@" + str(nargs) + "\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n" \
                        "@SP\nD=M\n@LCL\nM=D\n@" + func_name + "\n0;JMP\n(" + returnAdd + ")\n"
        Dictionaries.ret_count += 1
        self.file.write(write_command)

    def TemplatePop(self, segment, index):

        if (segment in Dictionaries.segments):

            if segment == "static":
                return "@SP\nM=M-1\nA=M\nD=M\n@" + str(self.filename) + "." + str(index) + "\nM=D\n"

            check = Dictionaries.segments[segment]
            temp = "A"
            if check in Dictionaries.helper_loop:
                temp = "M"
            return "@SP\nM=M-1\nA=M\nD=M\n@R13\nM=D\n@" + Dictionaries.segments[segment] + "\nD=" + temp + "\n@{0}\nD=D+A\n@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D\n".format(str(index))


    def TemplatePush(self, segment, index):
        """
        Template for push Command
        :param segment: segment type
        :param index: input of index
        """
        temp = "NONE"
        if "constant" in segment:
            return "@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str(index))
        elif segment in Dictionaries.segments:
            if segment == "static":
               return "@" +str(self.filename) + "." + str(index) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

            check = Dictionaries.segments[segment]
            if check in Dictionaries.helper_loop:
               temp = "A=D+A\nD=M\n"
            if segment == "pointer":
                temp = "D=D+A\nA=D\nD=M\n"
            if segment == "temp":
                temp = "A=D+A\nD=M"

            return "@" + Dictionaries.segments[segment] + "\nD=M\n@" + str(index) + "\n" + temp + "@SP\nA=M\nM=D\n@SP\nM=M+1\n"