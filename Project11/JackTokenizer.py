"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re
from pydoc import Helper

Term_Elem = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char",
             "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
Symbol = {"{", "}", "(", ")", "[", "]", ".", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~", '^', '#', ","}

keywordsRegex = '(?!\w)|'.join(Term_Elem) + '(?!\w)'
symbolsRegex = '[' + re.escape('|'.join(Symbol)) + ']'
integerRegex = r'\d+'
stringsRegex = r'"[^"\n]*"'
identifiersRegex = r'[\w]+'
pattern = re.compile(
    keywordsRegex + '|' + symbolsRegex + '|' + integerRegex + '|' + stringsRegex + '|' + identifiersRegex)


def tokenize(lst):
    return [word for word in split(lst)]


def split(line):
    return pattern.findall(line)


def remove_com_space(f):
    inp_lines_as_list = [line.rstrip("\n") for line in f]
    remove_new_lines = [val for val in inp_lines_as_list if val != "" or val != " "]
    remove_white = [val.strip() for val in remove_new_lines]

    lst = []
    prob = {"/*", "//", "*/"}
    flag = False

    for val in remove_white:
        # commands line or handle the /**---*/
        if len(val) >= 2 and val[:2] == "/*":
            flag = True
        if "*/" in val:
            flag = False
            continue
        if flag:
            continue
        if len(val) >= 2 and (val[:2] in prob):
            continue
        elif "//" in val:
            ind = val.find("//")
            new_val = val[:ind]
            lst.append(new_val)
        else:
            lst.append(val)

    new_check = [val for val in lst if val != "" or val != " "]

    nList = ''.join(new_check)
    lst = nList.split(" ")

    return tokenize(' '.join(lst))


class JackTokenizer:

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        self.currLine = 0
        self.input_lines = remove_com_space(input_stream)
        self.length = len(self.input_lines)

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here
        return self.currLine + 2 != self.length

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        if self.has_more_tokens():
            self.currLine += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """

        # Your code goes here!
        word = self.input_lines[self.currLine]
        if word in Term_Elem:
            return "keyword"
        if word[0] == '"':
            return "stringConstant"
        elif word in Symbol:
            return "symbol"
        elif word.isnumeric():
            return "integerConstant"
        return "identifier"

