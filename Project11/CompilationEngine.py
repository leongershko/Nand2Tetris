"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

# constants
classVar = {"static", "field"}
subDec = {"method", "constructor", "function"}
type = {"int", "char", "boolean"}
statements = {"let": "letStatement", "if": "ifStatement", "while": "whileStatement", "do": "doStatement",
              "return": "returnStatement"}
op = {"+": "add", "-": "sub", "*": "call Math.multiply 2", "/": "call Math.divide 2", "&": "and", "|": "or", "<": "lt",
      ">": "gt", "=": "eq"}
op_2 = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
unaryop = {'~': "not", '-': "neg", "^": "shiftleft", "#": "shiftright"}
Symbol = {"{", "}", "(", ")", "[", "]"}


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    ifCount = -1
    whileCount = -1

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output = output_stream
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(output_stream)
        self.class_name = ""

        # wordXML
        self.currWord = self.tokenizer.input_lines[self.tokenizer.currLine]
        self.nextWord = self.tokenizer.input_lines[self.tokenizer.currLine + 1]

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.advance()  # class
        self.class_name = self.currWord
        self.advance()  # class_name
        self.advance()  # {

        while self.tokenizer.has_more_tokens():
            if self.currWord not in subDec:
                self.compile_class_var_dec()
            elif self.currWord in subDec:
                self.compile_subroutine()
            else:
                self.advance()  # symbol

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        if self.currWord == "field" or self.currWord == "static":
            kind, type = self.currWord, self.nextWord
            self.advance()  # Kind
            self.advance()  # Type

            while self.currWord != ";":
                if self.currWord == ",":
                    self.advance()  # ,
                self.symbolTable.define(self.currWord, type, kind)
                self.advance()  # for getting new name
            self.advance()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        funType = self.currWord
        self.advance()  # advance func / const / method
        self.advance()  # Type
        funcName = self.class_name + "." + self.currWord
        self.advance()  # Name
        self.symbolTable.start_subroutine()
        self.compile_parameter_list(funType)

        # subroutineBody
        self.advance()  # {
        while self.currWord == "var":
            self.compile_var_dec()
        var_count = self.symbolTable.var_count("var", "sub")
        self.vmWriter.write_function(funcName, var_count)
        self.init_function(funType)

        # Statements
        while self.currWord in statements:
            self.compile_statements()
        self.advance()  # }

    def init_function(self, function_type):
        if function_type == "constructor":
            vars_count = self.symbolTable.var_count("field", "class")
            self.vmWriter.write_push("constant", vars_count)
            self.vmWriter.write_call("Memory.alloc", 1)
            self.vmWriter.write_pop("pointer", 0)
        elif function_type == "method":
            self.vmWriter.write_push("argument", 0)
            self.vmWriter.write_pop("pointer", 0)

    def compile_parameter_list(self, type) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        if type == "method":
            self.symbolTable.define("this", self.class_name, "arg")

        self.advance()  # (
        while self.currWord != ')':
            if self.currWord == ',':
                self.advance()
            self.symbolTable.define(self.nextWord, self.currWord, "arg")
            self.advance()  # type
            self.advance()  # name
        self.advance()  # )

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        kind, type = self.currWord, self.nextWord
        self.advance()  # var
        self.advance()  # type
        while self.currWord != ";":
            if self.currWord == ",":
                self.advance()
            self.symbolTable.define(self.currWord, type, kind)
            self.advance()
        self.advance()  # ;

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
        self.advance()  # do
        n_vars = 0
        caller = self.currWord
        self.advance()  # Caller_name
        self.subCase(caller)
        self.vmWriter.write_pop("temp", 0)
        self.advance()  # ;

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.advance()  # let
        name = self.currWord
        kindName = self.symbolTable.kind_of(name)
        indexName = self.symbolTable.index_of(name)
        self.advance()  # var name

        if self.currWord == "[":  # let arr[1] = arr[2]
            self.arrayExpression()
            self.vmWriter.write_push(kindName, int(indexName))
            self.vmWriter.write_arithmetic("add")

            self.advance()  # =
            self.compile_expression()
            self.advance()  # ;

            self.vmWriter.write_pop("temp", 0)
            self.vmWriter.write_pop("pointer", 1)
            self.vmWriter.write_push("temp", 0)

            self.vmWriter.write_pop("that", 0)

        else:
            self.advance()  # =
            self.compile_expression()
            self.vmWriter.write_pop(kindName, indexName)
            self.advance()  # ;

    def arrayExpression(self):
        self.advance()  # ( / [
        self.compile_expression()
        self.advance()  # ]

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.whileCount += 1
        whileCount = self.whileCount
        self.symbolTable.while_count += 1
        self.vmWriter.write_label("WHILE_L1_" + str(whileCount))

        self.advance()  # while
        self.advance()  # (
        self.compile_expression()
        self.vmWriter.write_arithmetic("not")

        self.advance()  # )
        self.advance()  # {

        self.vmWriter.write_if("WHILE_L2_" + str(whileCount))
        while self.currWord in statements:
            self.compile_statements()

        self.vmWriter.write_goto("WHILE_L1_" + str(whileCount))
        self.vmWriter.write_label("WHILE_L2_" + str(whileCount))
        self.advance()  # }

    def compile_return(self) -> None:
        """Compiles a return statement."""

        self.advance()  # return
        if self.currWord != ";":
            self.compile_expression()
        else:
            self.vmWriter.write_push("constant", 0)
            # todo Added this to check last tests can be removed
            self.vmWriter.write_pop("temp", 0)
        self.vmWriter.write_return()
        self.advance()  # ;

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.ifCount += 1
        ifCount = self.ifCount

        self.advance()  # if
        self.advance()  # (
        self.compile_expression()
        self.advance()  # )
        self.advance()  # {

        self.vmWriter.write_if("IF_L1_" + str(ifCount))
        self.vmWriter.write_goto("IF_L2_" + str(ifCount))
        self.vmWriter.write_label("IF_L1_" + str(ifCount))
        while self.currWord in statements:
            self.compile_statements()

        self.vmWriter.write_goto("END_IF_" + str(ifCount))
        self.advance()  # }
        self.vmWriter.write_label("IF_L2_" + str(ifCount))

        # else State
        if self.currWord == "else":
            self.advance()  # else
            self.advance()  # {
            while self.currWord in statements:
                self.compile_statements()
            self.advance()  # }

        self.vmWriter.write_label("END_IF_" + str(ifCount))

    def compile_expression(self) -> None:

        self.compile_term()
        while self.currWord in op:  # "2+3 -> 23+"
            operation = self.currWord
            self.advance()  # op
            self.compile_term()
            self.output.write(op[operation] + "\n")

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
        name = self.currWord
        if self.currWord in unaryop:
            op = self.currWord
            self.advance()
            self.compile_term()
            self.output.write(unaryop[op] + "\n")

        elif self.currWord == '(':
            self.advance()  # (
            self.compile_expression()
            self.advance()  # )

        elif self.currType == "stringConstant":
            a = self.currWord.replace('"', "")
            self.currWord = a.strip()
            self.vmWriter.write_push('constant', len(self.currWord))
            self.vmWriter.write_call("String.new", 1)
            for ch in self.currWord:
                self.vmWriter.write_push("constant", ord(ch))
                self.vmWriter.write_call("String.appendChar", 2)
            self.advance()

        elif self.currType == "integerConstant":
            self.vmWriter.write_push("constant", self.currWord)
            self.advance()

        elif self.currWord in constants:
            if self.currWord == "this":
                self.vmWriter.write_push('pointer', 0)
            else:
                self.vmWriter.write_push('constant', 0)
                if self.currWord == "true":
                    self.vmWriter.write_arithmetic("not")
            self.advance()

        else:  # case of the curr word is subroutine or var
            self.advance()
            if self.currWord == '[':
                # todo check if we need to put it after arrayExp
                self.arrayExpression()
                kindArr = self.symbolTable.kind_of(name)
                indexArr = self.symbolTable.index_of(name)
                self.vmWriter.write_push(kindArr, indexArr)  # (push arg\var..) 1

                self.vmWriter.write_arithmetic("add")
                self.vmWriter.write_pop("pointer", 1)
                self.vmWriter.write_push("that", 0)

            elif self.currWord == '.' or self.currWord == "(":  # subroutine Call'
                self.subCase(name)

            else:
                kindVal = self.symbolTable.kind_of(name)
                indexVal = self.symbolTable.index_of(name)
                self.vmWriter.write_push(kindVal, indexVal)

    def subCase(self, name):
        num_vars = 0
        function = ""
        if self.currWord == '.':  # subroutine Call
            self.advance()  # .
            subName = self.currWord
            self.advance()  # subroutine Name
            nameType = self.symbolTable.type_of(name)

            if nameType != None:  # a = Leon.raz(x+5,y)
                kindName = self.symbolTable.kind_of(name)
                indexName = self.symbolTable.index_of(name)
                self.vmWriter.write_push(kindName, indexName)
                function = nameType + "." + subName
                num_vars += 1
            else:  # class - Create Object
                function = str(name + "." + subName)

        elif self.currWord == '(':
            function = str(self.class_name + "." + name)
            num_vars += 1
            self.vmWriter.write_push("pointer", 0)

        self.advance()  # (
        num_vars = int(self.compile_expression_list(num_vars))
        self.advance()  # )
        self.vmWriter.write_call(function, num_vars)

    def compile_expression_list(self, counter) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""

        while self.currWord != ")":
            if self.currWord == ",":
                self.advance()  # ,
                self.compile_expression()
                counter += 1
            else:
                self.compile_expression()
                counter += 1
        return counter
