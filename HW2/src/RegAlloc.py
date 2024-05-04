class RegisterAllocator_simp:
    reg_dict = {}
    def __init__(self, processor):
        self.processor = processor
        self.cnt = 0
    
    def allocate_registers(self, instructions, bundles):
        # phase 1
        # allocate in scheduled order
        # give dst reg a new name

        # for ins in instructions:
        #     if not ins.dst in {None, "LC", "EC"} :
        #         self.cnt += 1
        #         self.reg_dict[ins.dst] = "x" + str(self.cnt)
        #         ins.dst_new = self.reg_dict[ins.dst]
        #     else:
        #         ins.dst_new = ins.dst

        for bundle in bundles:
            for ins in bundle:
                if ins is not None:
                    if not ins.dst in {None, "LC", "EC"} :
                        self.cnt += 1
                        self.reg_dict[ins.dst] = "x" + str(self.cnt)
                        ins.dst_new = self.reg_dict[ins.dst]
                    else:
                        ins.dst_new = ins.dst

        # phase 2
        # rename the src/opA/opB/addr with the new name
        # if interloop dependency with multiple possibilities, use the BB0 name
        for ins in instructions:
            # print(ins)
            # print(ins.local_dependencies)
            # local dependency
            for (opname, id) in ins.local_dependencies:
                if opname == 'opA':
                    ins.opA_new = instructions[id].dst_new
                if opname == 'opB':
                    ins.opB_new = instructions[id].dst_new
                if opname == 'src':
                    ins.src_new = instructions[id].dst_new
                if opname == 'addr':
                    ins.addr_new = instructions[id].dst_new

            # TODO: interloop dependency
            # TODO: post loop dependency
            # TODO: loop invariant
        
        # phase 3
        # 

        # phase 4
        for bundle in bundles:
            for ins in bundle:
                # print(ins)
                # import ipdb; ipdb.set_trace()
                if ins is not None:
                    if ins.opA is not None and ins.opA_new is None:
                        self.cnt += 1
                        ins.opA_new = "x" + str(self.cnt)
                    if ins.opB is not None and ins.opB_new is None:
                        self.cnt += 1
                        ins.opB_new = "x" + str(self.cnt)
                    if ins.src is not None and ins.src_new is None:
                        self.cnt += 1
                        ins.src_new = "x" + str(self.cnt)
                    if ins.addr is not None and ins.addr_new is None:
                        self.cnt += 1
                        ins.addr_new = "x" + str(self.cnt)
        
        pass