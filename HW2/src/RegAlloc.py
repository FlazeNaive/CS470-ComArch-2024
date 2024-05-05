from Scheduler import Scheduler
from Instruction import Instruction

class RegisterAllocator_pip:
    reg_dict = {}
    ins_stage = []
    
    def __init__(self, processor):
        self.processor = processor
        self.cnt_reg_nonrot = 0
        self.cnt_reg = 0
        self.reg_base = 32
    
    nonvar_ins = set()

    def simp_alloc(self, instructions, BB, bundles):
        for bundle in bundles:
            for ins in bundle:
                if ins is None or ins == '--':
                    continue
                if ins.dst not in {None, "LC", "EC"} and ins.dst_new is None:
                    self.cnt_reg_nonrot += 1
                    ins.dst_new = "x" + str(self.cnt_reg_nonrot)
        for ins in BB:
            for (opname, id) in ins.local_dependencies:
                if getattr(ins, opname + "_new") is None:
                    setattr(ins, opname + "_new", instructions[id].dst_new)

    def allocate_registers(self, instructions, scheduler, BB0, BB1, BB2):
        self.ins_stage = [None for i in range(len(instructions) + 1)]

        # phase1
        for bundle in scheduler.bundles:
            for ins in bundle:
                if ins is not None and ins != '--':
                    if ins.dst in {"LC", "EC"}:
                        ins.dst_new = ins.dst
        
        cnt_stage = 0
        cnt_in_stage = 0
        for bundle in scheduler.bundles[scheduler.time_start_of_loop : scheduler.time_end_of_loop]:
            for ins in bundle:
                if ins is not None and ins != '--':
                    self.ins_stage[ins.id] = cnt_stage
                    if ins.dst not in {None, "LC", "EC"}:
                        ins.dst_new = "x" + str(self.reg_base + self.cnt_reg * scheduler.II)
                        self.cnt_reg += 1
            cnt_in_stage += 1
            if cnt_in_stage == scheduler.II:
                cnt_in_stage = 0
                cnt_stage += 1

        # phase2
        for ins in instructions:
            for (opname, id) in ins.loop_invariant:
                # import ipdb; ipdb.set_trace()
                self.nonvar_ins.add(id)
                
        print(self.nonvar_ins)
        for nonvar_id in self.nonvar_ins:
            self.cnt_reg_nonrot += 1
            # import ipdb; ipdb.set_trace()
            instructions[nonvar_id].dst_new = "x" + str(self.cnt_reg_nonrot)


        # phase3
        for ins in BB1:
            for (opname, id) in ins.loop_invariant:
                setattr(ins, opname + "_new", instructions[id].dst_new)
            
            for (opname, id) in ins.local_dependencies:
                St_D = self.ins_stage[ins.id]
                St_S = self.ins_stage[id]
                src_reg = instructions[id].dst_new
                src_reg_id = int(src_reg[1:])
                new_reg_id = src_reg_id + (St_D - St_S)
                # print(src_reg_id)
                # print(new_reg_id)
                # print("")
                setattr(ins, opname + "_new", "x" + str(new_reg_id))
                
            for (opname) in ins.interloop_dependencies:
                # print(ins)
                # import ipdb; ipdb.set_trace()
                aim_ins = ins.interloop_dependencies[opname]['BB1']
                St_D = self.ins_stage[ins.id]
                St_S = self.ins_stage[aim_ins]
                src_reg = instructions[aim_ins].dst_new
                src_reg_id = int(src_reg[1:])
                new_reg_id = src_reg_id + (St_D - St_S) + 1
                setattr(ins, opname + "_new", "x" + str(new_reg_id))
                
                
        # phase 4
        for ins in BB1:
            for (opname) in ins.interloop_dependencies:
                BB0_id = ins.interloop_dependencies[opname]['BB0']
                BB1_id = ins.interloop_dependencies[opname]['BB1']
                src_reg = instructions[BB1_id].dst_new
                src_reg_id = int(src_reg[1:])
                stage_offset = -self.ins_stage[BB1_id]
                iter_offset = 1
                new_reg_id = src_reg_id + stage_offset + iter_offset
                instructions[BB0_id].dst_new = "x" + str(new_reg_id)

            # within BB0/BB2
        self.simp_alloc(instructions, BB0, scheduler.bundles[:scheduler.time_start_of_loop])
        self.simp_alloc(instructions, BB2, scheduler.bundles[scheduler.time_end_of_loop:])

        for ins in BB2:
            for (opname, id) in ins.post_loop_dependencies:
                src_reg = instructions[id].dst_new
                src_reg_id = int(src_reg[1:])
                iter_offset = 0
                max_stage = 0
                for i in range(len(instructions) + 1):
                    if self.ins_stage[i] is not None:
                        max_stage = max(max_stage, self.ins_stage[i])
                stage_offset = max_stage - self.ins_stage[id]
                new_reg_id = src_reg_id + stage_offset + iter_offset
                setattr(ins, opname + "_new", "x" + str(new_reg_id))


        scheduler.print()
        # print(scheduler.bundles[1][1])
        # print(scheduler.bundles[1][1].dst_new)
        # print(instructions[3])
        # print(instructions[3].dst_new)
        pass

class RegisterAllocator_simp:
    reg_dict = {}
    need_mov_phase3 = set()

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
                    self.need_mov_phase3.add((BB0_id, BB1_id))

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