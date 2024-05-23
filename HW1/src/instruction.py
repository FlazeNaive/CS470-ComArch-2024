# instruction.py

class Instruction:
    opcode = None
    dest = None
    opA_ori = None
    opB_ori = None
    opA_phy = None
    opB_phy = None
    imm = None
    def __init__(self, instruction):
        parts = instruction.split()
        self.opcode = parts[0]
        operands = parts[1:]
        for operand in operands[:-1]:
            if operand[-1] == ',':
                operands[operands.index(operand)] = operand[:-1]
        self.dest = int(operands[0][1:])
        self.opA_ori = int(operands[1][1:])
        if self.opcode == 'addi':
            self.opB_ori = int(operands[2])
            self.imm = self.opB_ori
        else:
            self.opB_ori = int(operands[2][1:])