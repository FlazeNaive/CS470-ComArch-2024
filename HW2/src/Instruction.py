class Instruction:
    ALU_OPS = ["add", "sub", "mulu", "addi"]
    MEM_OPS = ["ld", "st"]
    LOOP_OPS = ["loop", "loop.pip"]
    NOP_OPS = ["nop"]
    MOV_OPS = ["mov"]

    def __init__(self, text):
        self.operation, self.operands = self.parse_instruction(text)
        self.opA = None
        self.opB = None

        self.dst = None
        self.src = None

        self.immediate = None
        self.addr = None

        self.loopStart = None

        self.pX = None
        self.LC = None
        self.EC = None


        if self.operation in self.ALU_OPS:
            self.dst = self.operands[0]
            self.opA = self.operands[1]
            if self.operation == "addi":
                self.immediate = self.operands[2]
            else:
                self.opB = self.operands[2]
        
        if self.operation in self.MEM_OPS:
            self.dst = self.operands[0]
            self.immediate = self.operands[1].split("(")[0]
            self.addr = self.operands[1].split("(")[1].split(")")[0]
            
            print("dst: ", self.dst)
            print("immediate: ", self.immediate)
            print("addr: ", self.addr)
        
        if self.operation in self.LOOP_OPS:
            self.loopStart = self.operands[0]
        
        if self.operation in self.NOP_OPS:
            pass
        
        if self.operation in self.MOV_OPS:
            self.dst = self.operands[0]
            self.src = self.operands[1]
        
        self.immediate = int(self.immediate) if self.immediate is not None else None
    
    def parse_instruction(self, text):
        # Parse the instruction text and return the operation and operands
        parts = text.split()
        return parts[0], parts[1:]
    
    def __str__(self):
        return "{} {}".format(self.operation, " ".join(self.operands))