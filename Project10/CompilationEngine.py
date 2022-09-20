"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from JackTokenizer import JackTokenizer

classVar = {"static", "field"}
subDec = {"method", "constructor", "function"}
type = {"int", "char", "boolean"}
statements = {"let": "letStatement", "if": "ifStatement", "while": "whileStatement", "do": "doStatement",
              "return": "returnStatement"}
op = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
op_2 = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
unaryop = ['~', '-', "^", "#"]


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        # Your code goes here!
        self.tokenizer = input_stream
        self.output = output_stream
        self.currWord = self.tokenizer.input_lines[self.tokenizer.currLine]
        self.nextWord = self.tokenizer.input_lines[self.tokenizer.currLine + 1]
        self.currType = self.tokenizer.token_type()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # self.writeOpenToken("token")

        if self.currWord == "class":
            self.writeOpenToken("class")
            self.writeToken()
            self.advance()
            self.writeToken()  # className
            self.advance()
            self.writeToken()  # {
            self.advance()

            while self.tokenizer.has_more_tokens():
                if self.currWord not in subDec:
                    self.compile_class_var_dec()
                elif self.currWord in subDec:
                    self.compile_subroutine()
                else:
                    self.writeToken()
                    self.advance()
        self.writeToken()
        self.output.write("</class>")

    def writeToken(self):
        if self.currWord in op_2:
            self.currWord = op_2[self.currWord]
        self.output.write("<{0}> {1} </{0}>\n".format(self.currType, self.currWord))

    def writeOpenToken(self, label):
        self.output.write("<{0}>\n".format(label))

    def writeCloseToken(self, label):
        self.output.write("</{0}>\n".format(label))

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.writeOpenToken("classVarDec")
        while self.currWord != ";":
            self.writeToken()
            self.advance()
        if self.currWord == ";":
            self.writeToken()
            self.advance()
        self.writeCloseToken("classVarDec")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.writeOpenToken("subroutineDec")
        self.writeToken()  # func / const / method
        self.advance()
        self.writeToken()  # type
        self.advance()
        self.writeToken()  # subroutineName
        self.advance()
        self.compile_parameter_list()

        # subroutineBody
        self.writeOpenToken("subroutineBody")
        self.writeToken()  # {
        self.advance()
        while self.currWord == "var":
            self.writeOpenToken("varDec")
            self.compile_var_dec()
        if self.currWord in statements:
            self.writeOpenToken("statements")
        while self.currWord in statements:
            self.compile_statements()

        self.writeCloseToken("statements")
        self.writeToken()  # }
        self.advance()

        self.writeCloseToken("subroutineBody")
        self.writeCloseToken("subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.writeToken()  # (
        self.advance()
        self.writeOpenToken("parameterList")
        while self.currWord != ')':
            self.writeToken()
            self.advance()

        self.writeCloseToken("parameterList")
        self.writeToken()  # )
        self.advance()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        while self.currWord != ";":
            self.writeToken()
            self.advance()
        if self.currWord == ";":
            self.writeToken()
            self.advance()
        self.writeCloseToken("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        if self.currWord == "do":
            self.compile_do()
        elif self.currWord == "let":
            self.compile_let()
        elif self.currWord == "while":
            self.compile_while()
        elif self.currWord == "if":
            self.compile_if()
        elif self.currWord == "return":
            self.compile_return()

    def advance(self):
        if self.tokenizer.currLine + 2 != self.tokenizer.length:
            self.tokenizer.advance()
            self.currType = self.tokenizer.token_type()  # update type
            self.currWord = self.tokenizer.input_lines[self.tokenizer.currLine]
            self.nextWord = self.tokenizer.input_lines[self.tokenizer.currLine + 1]

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # flag = None
        self.writeOpenToken("doStatement")
        while self.currWord != ";":
            self.writeToken()  # subroutine Call / )
            self.advance()
            if self.currWord == "(":
                self.compile_expression_list()

        self.writeToken()  # ;
        self.advance()
        self.writeCloseToken("doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement."""

        self.writeOpenToken("letStatement")
        self.writeToken()  # let
        self.advance()
        self.writeToken()  # var name
        self.advance()
        if self.currWord == "[":
            self.arrayExpression()
        self.writeToken()  # =
        self.advance()
        self.compile_expression()
        self.writeToken()  # ;
        self.advance()
        self.writeCloseToken("letStatement")

    def arrayExpression(self):
        self.writeToken()  # ( / [
        self.advance()
        self.compile_expression()
        self.writeToken()  # ]
        self.advance()

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.writeOpenToken("whileStatement")
        self.writeToken()  # while
        self.advance()
        self.writeToken()  # (
        self.advance()
        self.compile_expression()
        self.writeToken()  # )
        self.advance()
        self.writeToken()  # {
        self.advance()
        if self.currWord in statements:
            self.writeOpenToken("statements")
        while self.currWord in statements:
            self.compile_statements()

        self.writeCloseToken("statements")
        self.writeToken()  # }
        self.advance()
        self.writeCloseToken("whileStatement")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.writeOpenToken("returnStatement")
        self.writeToken()  # return
        self.advance()
        if self.currWord != ";":
            self.compile_expression()
        self.writeToken()  # ;
        self.advance()
        self.writeCloseToken("returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.writeOpenToken("ifStatement")
        self.writeToken()  # if
        self.advance()
        self.writeToken()  # (
        self.advance()
        self.compile_expression()
        self.writeToken()  # )
        self.advance()
        self.writeToken()  # {
        self.advance()
        if self.currWord in statements:
            self.writeOpenToken("statements")
        while self.currWord in statements:
            self.compile_statements()
        self.writeCloseToken("statements")
        self.writeToken()  # }
        self.advance()

        # else State
        if self.currWord == "else":
            self.writeToken()  # else
            self.advance()
            self.writeToken()  # {
            self.advance()
            if self.currWord in statements:
                self.writeOpenToken("statements")
            while self.currWord in statements:
                self.compile_statements()

            self.writeCloseToken("statements")
            self.writeToken()  # }
            self.advance()

        self.writeCloseToken("ifStatement")

    def check_exp_list(self):
        temp_cur = self.tokenizer.currLine
        while self.currWord != ";" and self.currWord != ")":
            if self.currWord == ",":
                self.tokenizer.currLine = temp_cur  # init currLine again
                return True
            self.advance()
        # init args again
        self.tokenizer.currLine = temp_cur
        self.currWord = self.tokenizer.input_lines[self.tokenizer.currLine]
        self.nextWord = self.tokenizer.input_lines[self.tokenizer.currLine + 1]

        self.currType = self.tokenizer.token_type()
        return False

    def compile_expression(self) -> None:
        self.writeOpenToken("expression")
        self.compile_term()
        while self.currWord in op:
            self.writeToken()  # op
            self.advance()
            self.compile_term()
        self.writeCloseToken("expression")

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        constants = ["true", "false", "this", "null"]

        self.writeOpenToken("term")
        if self.currWord in unaryop:
            self.writeToken()
            self.advance()
            self.compile_term()
        elif self.currWord == '(':
            self.writeToken()  # (
            self.advance()
            self.compile_expression()
            self.writeToken()  # )
            self.advance()
        else:
            # identifier
            if self.currType == "stringConstant":
                a = self.currWord.replace('"', "")
                self.currWord = a.strip()
            self.writeToken()
            self.advance()

            if self.currWord == '[':
                self.arrayExpression()
            elif self.currWord == '.':
                self.writeToken()  # .
                self.advance()
                self.writeToken()  # subroutine Name
                self.advance()
                self.compile_expression_list()
                self.writeToken()  # )
                self.advance()
            elif self.currWord == '(':
                self.compile_expression_list()
                self.writeToken()  # )
                self.advance()
        self.writeCloseToken("term")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.writeToken()  # (
        self.advance()
        self.writeOpenToken("expressionList")
        while self.currWord != ")":

            if self.currWord == ",":
                self.writeToken()  # ,
                self.advance()
                self.compile_expression()
            else:
                self.compile_expression()

        self.writeCloseToken("expressionList")
