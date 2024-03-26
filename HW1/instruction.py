# instruction.py
def decode_instruction(instruction):
    parts = instruction.split()
    opcode = parts[0]
    operands = parts[1:]
    return opcode, operands