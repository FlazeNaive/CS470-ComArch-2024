class RegisterAllocator_simp:
    reg_dict = {}
    def __init__(self, processor):
        self.processor = processor
        self.cnt = 0
    
    def allocate_registers(self, instructions):
        # phase 1
        # allocate in scheduled order
        # give dst reg a new name

        for ins in instructions:
            if not ins.dst in {None, "LC", "EC"} :
                self.cnt += 1
                self.reg_dict[ins.dst] = "x" + str(self.cnt)
                ins.dst_new = self.reg_dict[ins.dst]

        # phase 2
        # rename the src/opA/opB with the new name
        # if interloop dependency with multiple possibilities, use the BB0 name
        for ins in instructions:
            # local dependency
            for (opname, id) in ins.local_dependencies:
                if opname == 'opA':
                    ins.opA_new = instructions[id].dst_new
                if opname == 'opB':
                    ins.opB_new = instructions[id].dst_new
                if opname == 'src':
                    ins.src_new = instructions[id].dst_new
        
        # phase 3
        # 
        pass