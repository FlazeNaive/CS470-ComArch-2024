# instruction.py
import re

def decode_instruction(instruction):
    parts = instruction.split()
    opcode = parts[0]
    operands = parts[1:]
    for operand in operands[:-1]:
        if operand[-1] == ',':
            operands[operands.index(operand)] = operand[:-1]

    return opcode, operands