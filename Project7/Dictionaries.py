segments = {"local": "LCL", "argument": "ARG", "pointer 0": "THIS",
            "pointer 1": "THAT", "that": "THAT", "this": "THIS", "static": "STATIC", "temp": "R5", "pointer": None}
arithmetic1 = {"add": "M=D+M", "sub": "M=M-D", "and": "M=D&M", "or": "M=D|M", }
arithmetic2 = {"gt": ["JGE", "JLE", "JGT"], "lt": ["JLE", "JGE", "JLT"], "eq": "JEQ", "neg": None, "not": None}
