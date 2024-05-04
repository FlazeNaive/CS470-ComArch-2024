class Instruction:
    MUL_OPS = ["mulu"]
    ALU_OPS = ["add", "sub", "mulu", "addi"]
    MEM_OPS = ["ld", "st"]
    LOOP_OPS = ["loop", "loop.pip"]
    NOP_OPS = ["nop"]
    MOV_OPS = ["mov"]

    def __init__(self, text, id=None):
        # import ipdb; ipdb.set_trace()
        self.id = id

        self.operation, self.operands = self.parse_instruction(text)
        self.dst = None
        self.dst_new = None

        self.opA = None
        self.opB = None
        self.src = None
        self.addr = None
        self.opA_new = None
        self.opB_new = None
        self.src_new = None
        self.addr_new = None

        self.bool = None
        self.immediate = None

        self.loopStart = None

        self.pX = None
        self.LC = None
        self.EC = None

        # === Dependencies ===
        self.local_dependencies = []                # [(opname, id_instruction)]
        self.interloop_dependencies = {}            # {opname: {'BB0': id_ins, 'BB1': id_ins} }
        self.post_loop_dependencies = []
        self.loop_invariant = []

        if self.operation in self.ALU_OPS:
            self.dst = self.operands[0]
            self.opA = self.operands[1]
            if self.operation == "addi":
                self.immediate = self.operands[2]
            else:
                self.opB = self.operands[2]
        
        if self.operation in self.MEM_OPS:
            if self.operation == "ld":
                self.dst = self.operands[0]
            elif self.operation == "st":
                self.src = self.operands[0]
            self.immediate = self.operands[1].split("(")[0]
            self.addr = self.operands[1].split("(")[1].split(")")[0]
            
            # print("dst: ", self.dst)
            # print("immediate: ", self.immediate)
            # print("addr: ", self.addr)
        
        if self.operation in self.LOOP_OPS:
            self.loopStart = self.operands[0]
        
        if self.operation in self.NOP_OPS:
            pass
        
        if self.operation in self.MOV_OPS:
            self.dst = self.operands[0]
            if self.operands[1].isdigit():
                self.immediate = self.operands[1]
            elif self.operands[1] in ("true", "false"):
                # actually won't happen in the input
                self.bool = self.operands[1]
            else:
                self.src = self.operands[1]
        
        # self.immediate = int(self.immediate) if self.immediate is not None else None
        self.loopStart = int(self.loopStart) if self.loopStart is not None else None
    
    def parse_instruction(self, text):
        # Parse the instruction text and return the operation and operands
        parts = text.split()
        parts = [p.strip(",") for p in parts]
        return parts[0], parts[1:]
    
    def __str__(self):
        return "{} {}".format(self.operation, " ".join(self.operands))
    
    def str_new(self):
        rtn = "{} ".format(self.operation)

        if self.operation in self.ALU_OPS:
            rtn += "{}, {}, ".format(self.dst_new, self.opA_new)
            if self.operation == "addi":
                rtn += "{}".format(self.immediate)
            else:
                rtn += "{}".format(self.opB_new)

        if self.operation in self.MEM_OPS:
            if self.operation == "ld":
                rtn += "{}, ".format(self.dst_new)
            elif self.operation == "st":
                rtn += "{}, ".format(self.src_new)
            rtn += "{}({})".format(self.immediate, self.addr_new)

        if self.operation in self.LOOP_OPS:
            rtn += "{}".format(self.loopStart)

        if self.operation in self.NOP_OPS:
            rtn 

        if self.operation in self.MOV_OPS:
            rtn += "{}, ".format(self.dst_new)
            if self.immediate is not None:
                rtn += "{}".format(self.immediate)
            elif self.bool is not None:
                rtn += "{}".format(self.bool)
            else:
                rtn += "{}".format(self.src_new)

        return rtn


CONST_NOP = Instruction("nop")