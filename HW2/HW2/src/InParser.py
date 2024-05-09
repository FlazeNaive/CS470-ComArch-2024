import json
from Instruction import Instruction

def parse_input(input_json):
    with open(input_json, 'r') as file:
        data = json.load(file)
    return [Instruction(line, id) for id, line in enumerate(data)]

def parse_blockes(instructions):
    flag_has_loop = False
    loop_start = None
    BB0 = []
    BB1 = []
    BB2 = []

    for ins in instructions:
        # debug_print_ins(ins)
        if ins.operation == "loop":
            loop_start = ins.loopStart
            continue 

    if loop_start is None:
        BB0 = instructions
    else:
        for id, ins in enumerate(instructions):
            if id < loop_start:
                BB0.append(ins)
                continue
            if id >= loop_start:
                if not flag_has_loop:
                    BB1.append(ins)
                    if ins.operation == "loop":
                        flag_has_loop = True
                        continue
                else:
                    BB2.append(ins)

    return BB0, BB1, BB2, flag_has_loop, loop_start