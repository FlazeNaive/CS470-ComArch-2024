from Scheduler import Scheduler_simp
from Instruction import Instruction


class RegisterAllocator_simp:
    reg_dict = {}
    need_mov_phase3 = []

    def __init__(self, processor):
        self.processor = processor
        self.cnt = 0
    
    def allocate_registers(self, instructions, scheduler):
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

        for bundle in scheduler.bundles:
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
            # post loop dependency
            for (opname, id) in ins.post_loop_dependencies:
                if opname == 'opA':
                    ins.opA_new = instructions[id].dst_new
                if opname == 'opB':
                    ins.opB_new = instructions[id].dst_new
                if opname == 'src':
                    ins.src_new = instructions[id].dst_new
                if opname == 'addr':
                    ins.addr_new = instructions[id].dst_new
            # loop invariant
            for (opname, id) in ins.loop_invariant:
                if opname == 'opA':
                    ins.opA_new = instructions[id].dst_new
                if opname == 'opB':
                    ins.opB_new = instructions[id].dst_new
                if opname == 'src':
                    ins.src_new = instructions[id].dst_new
                if opname == 'addr':
                    ins.addr_new = instructions[id].dst_new
        
            # TODO: interloop dependency
            for opname in ins.interloop_dependencies:
                if 'BB0' in ins.interloop_dependencies[opname]:
                    opname_new = opname + "_new"
                    BB0_id = ins.interloop_dependencies[opname]['BB0']
                    BB1_id = ins.interloop_dependencies[opname]['BB1']
                    BB0_reg = instructions[BB0_id].dst_new
                    setattr(ins, opname_new, BB0_reg)
                    # import ipdb; ipdb.set_trace()

                    # 把 BB1_id那条insttruction的 dest register的值 mov到 -> BB0对应 那个
                    self.need_mov_phase3.append((BB0_id, BB1_id))

        # phase 3
        # BB1_reg -> BB0_reg

        for movs in self.need_mov_phase3:
            BB0_id, BB1_id = movs
            BB0_reg = instructions[BB0_id].dst_new
            BB1_reg = instructions[BB1_id].dst_new

            lowest_time = scheduler.time_end_of_loop
            ins_latency = 1
            if instructions[BB1_id].operation in scheduler.MUL_OPS:
                ins_latency = 3
            lowest_time = max(lowest_time,
                                scheduler.time_table[BB1_id] + ins_latency)
            new_mov_instruction = Instruction("mov " + BB0_reg + " " + BB1_reg)
            new_mov_instruction.dst_new = new_mov_instruction.dst
            new_mov_instruction.src_new = new_mov_instruction.src
            flag_inserted = scheduler.insert_endofloop(new_mov_instruction, lowest_time)
            

        # phase 4
        for bundle in scheduler.bundles:
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