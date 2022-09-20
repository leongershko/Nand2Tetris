segments = {"local": "LCL", "argument": "ARG","pointer":"R3", "that": "THAT", "this": "THIS", "static": "STATIC", "temp": "R5"}
arithmetic1 = {"add": "M=D+M", "sub": "M=M-D", "and": "M=D&M", "or": "M=D|M"}
arithmetic2 = {"gt": ["JGE", "JLE", "JGT"], "lt": ["JLE", "JGE", "JLT"], "eq": "JEQ", "neg": None, "not": None}
shifts = ["shiftleft", "shiftright"]
helper_loop = ["LCL", "ARG", "THIS", "THAT"]
ret_count = 1
loop_count = 1