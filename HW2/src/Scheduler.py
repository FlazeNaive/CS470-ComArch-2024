from math import ceil
from Instruction import Instruction

class Scheduler:
    MUL_OPS = ["mulu"]
    ALU_OPS = ["add", "sub", "mov", "addi"]
    MEM_OPS = ["ld", "st"]
    LOOP_OPS = ["loop", "loop.pip"]

    NOP_OPS = ["nop"]


    def __init__(self, processor):
        self.stages = []                          # 每个stage里有哪些bundle

        self.bundles = []                        # [(ALU0, ALU1, Mult, Mem, Branch)]
        self.predicator = []
        self.time_table = []                     # [id_bundle], 下表是id_instruction
        self.processor = processor

        self.II = 0

        self.time_start_of_loop = 0
        self.time_end_of_loop = 0

    def insert_prepareLoop(self, ins):
        cur_time = self.time_start_of_loop - 1
        if self.bundles[cur_time][0] == None:
            self.bundles[cur_time][0] = ins
        elif self.bundles[cur_time][1] == None:
            self.bundles[cur_time][1] = ins
        else:
            self.bundles.insert(cur_time + 1, [None, None, None, None, None])
            self.time_start_of_loop += 1
            self.time_end_of_loop += 1
            cur_time += 1
            self.bundles[cur_time][0] = ins
    
    def insert_ASAP(self, ins, id_low):
        flag_inserted = False
        for i_bundle in range(id_low, len(self.bundles)):
            if ins.operation in self.ALU_OPS:
                if self.bundles[i_bundle][0] == None:
                    self.bundles[i_bundle][0] = ins
                    self.time_table[ins.id] = i_bundle
                    flag_inserted = True
                    break
                elif self.bundles[i_bundle][1] == None:
                    self.bundles[i_bundle][1] = ins
                    self.time_table[ins.id] = i_bundle
                    flag_inserted = True
                    break
            if ins.operation in self.MUL_OPS:
                if self.bundles[i_bundle][2] == None:
                    self.bundles[i_bundle][2] = ins
                    self.time_table[ins.id] = i_bundle
                    flag_inserted = True
                    break
            if ins.operation in self.MEM_OPS:
                if self.bundles[i_bundle][3] == None:
                    self.bundles[i_bundle][3] = ins
                    self.time_table[ins.id] = i_bundle
                    flag_inserted = True
                    break
            if ins.operation in self.LOOP_OPS:
                if self.bundles[i_bundle][4] == None:
                    self.bundles[i_bundle][4] = ins
                    self.time_table[ins.id] = i_bundle
                    flag_inserted = True
                    break

        return flag_inserted
    
    def insert_ASAP_pip(self, ins, id_low):
        flag_inserted = self.insert_ASAP(ins, id_low)
        # print("inserting: ", ins.id)
        # print(ins)
        # print("id_low: ", id_low)
        # print(flag_inserted)
        # print("")

        if not flag_inserted:
            return False
        # import ipdb; ipdb.set_trace()
        cur_time = self.time_table[ins.id]
        for i_bundle in range(self.time_start_of_loop, len(self.bundles)):
            if i_bundle != cur_time and (i_bundle - cur_time) % self.II == 0:
                for j_unit in range(0, 5):
                    if self.bundles[cur_time][j_unit] != None and self.bundles[i_bundle][j_unit] == None:
                        self.bundles[i_bundle][j_unit] = '--'
        return True

    def insert_endofloop(self, ins, lowest_time=0):
        # import ipdb; ipdb.set_trace()
        cur_try = self.time_end_of_loop
        while cur_try < lowest_time:
            cur_try += 1
            self.bundles.insert(cur_try, [None, None, None, None, None])
            self.bundles[cur_try][4] = self.bundles[cur_try - 1][4]
            self.bundles[cur_try - 1][4] = None
            
        if self.bundles[cur_try][0] == None:
            self.bundles[cur_try][0] = ins
        elif self.bundles[cur_try][1] == None:
            self.bundles[cur_try][1] = ins
        else:
            cur_try += 1
            self.bundles.insert(cur_try, [None, None, None, None, None])
            self.bundles[cur_try][4] = self.bundles[cur_try - 1][4]
            self.bundles[cur_try - 1][4] = None
            self.bundles[cur_try][0] = ins
        self.time_end_of_loop = cur_try

    def append(self, ins, lowest_time=0):
        # import ipdb; ipdb.set_trace()
        self.bundles.append([None, None, None, None, None])
        while len(self.bundles) <= lowest_time:
            self.bundles.append([None, None, None, None, None])
        count_bundles = len(self.bundles) - 1
        self.time_table[ins.id] = count_bundles
        if ins.operation in self.ALU_OPS:
            self.bundles[count_bundles][0] = ins
        if ins.operation in self.MUL_OPS:
            self.bundles[count_bundles][2] = ins
        if ins.operation in self.MEM_OPS:
            self.bundles[count_bundles][3] = ins
        if ins.operation in self.LOOP_OPS:
            self.bundles[count_bundles][4] = ins
    
    def spread_reserved(self):
        cur_i_bundle = len(self.bundles) - 1
        # print("cur_i_bundle: ", cur_i_bundle)
        # for ins in self.bundles[cur_i_bundle]:
        #     print(ins, end="\t\t")
        # print()
        
        # import ipdb; ipdb.set_trace()
        for i in range(self.time_start_of_loop, cur_i_bundle):
            # print("i = ", i)
            # print("cur_bundle = ", self.bundles[i])
            # import ipdb; ipdb.set_trace()
            if (cur_i_bundle - i) % self.II == 0:
                for j_unit in range(0, 5):
                    if self.bundles[i][j_unit] != None:
                        self.bundles[cur_i_bundle][j_unit] = "--"
                    if self.bundles[cur_i_bundle][j_unit] != None and self.bundles[i][j_unit] == None:
                        self.bundles[i][j_unit] = "--"
            
    def append_pip(self, ins, lowest_time=0):
        # print(ins.id)
        # print(ins)

        # import ipdb; ipdb.set_trace()
        count_bundles = len(self.bundles) 
        self.bundles.append([None, None, None, None, None])
        self.spread_reserved()

        while len(self.bundles) <= lowest_time:
            self.bundles.append([None, None, None, None, None])
            self.spread_reserved()
        
        flag_inserted = False
        count_bundles = len(self.bundles) - 1
        while not flag_inserted:
            if ins.operation in self.ALU_OPS:
                if self.bundles[count_bundles][0] == None:
                    self.bundles[count_bundles][0] = ins
                    flag_inserted = True
                elif self.bundles[count_bundles][1] == None:
                    self.bundles[count_bundles][1] = ins
                    flag_inserted = True
            elif ins.operation in self.MUL_OPS:
                if self.bundles[count_bundles][2] == None:
                    self.bundles[count_bundles][2] = ins
                    flag_inserted = True
            elif ins.operation in self.MEM_OPS:
                if self.bundles[count_bundles][3] == None:
                    self.bundles[count_bundles][3] = ins
                    flag_inserted = True
            # elif ins.operation in self.LOOP_OPS:
            #     if self.bundles[count_bundles][4] == None:
            #         self.bundles[count_bundles][4] = ins
            #         flag_inserted = True
            if not flag_inserted:
                self.bundles.append([None, None, None, None, None])
                self.spread_reserved()
                count_bundles = len(self.bundles) - 1
            else:
                self.spread_reserved()

        count_bundles = len(self.bundles) - 1
        self.time_table[ins.id] = count_bundles
    

    def schedule_BB0(self, instructions, BB0):
        flag_added = [False for i in range(0, len(BB0))]
        cnt_left = len(BB0)

        for ins in BB0:
            flag_inserted = False
            lowest_time = 0
            if ins.local_dependencies == []:
                flag_inserted = self.insert_ASAP(ins, 0)
            else:
                for (opname, id) in ins.local_dependencies:
                    # id 是 dependency的指令的id
                    # 所以可以直接通过instruction[id]来访df
                    aim_ins = instructions[id]
                    ins_latency = 1
                    if aim_ins.operation in self.MUL_OPS:
                        ins_latency = 3
                    lowest_time = max(lowest_time, 
                                      self.time_table[aim_ins.id] + ins_latency)
                flag_inserted = self.insert_ASAP(ins, lowest_time) 

            if not flag_inserted:
                self.append(ins, lowest_time=lowest_time)


    def schedule_BB1(self, instructions, BB1):
        if len(BB1) == 0:
            return
        # import ipdb; ipdb.set_trace()
        lowest_time_start_loop = len(self.bundles)
        for ins in BB1:
            for (opname, id) in ins.loop_invariant:
                aim_ins = instructions[id]
                ins_latency = 1
                if aim_ins.operation in self.MUL_OPS:
                    ins_latency = 3
                lowest_time_start_loop = max(lowest_time_start_loop, 
                                              self.time_table[aim_ins.id] + ins_latency)
            for (opmap) in ins.interloop_dependencies:
                # import ipdb; ipdb.set_trace()
                # for BBname in ins.interloop_dependencies[opmap]:
                #    print(ins.interloop_dependencies[opmap][BBname])

                if 'BB0' in ins.interloop_dependencies[opmap]:
                    aim_ins = instructions[ ins.interloop_dependencies[opmap]['BB0'] ]
                    ins_latency = 1
                    if aim_ins.operation in self.MUL_OPS:
                        ins_latency = 3
                    lowest_time_start_loop = max(lowest_time_start_loop, 
                                                  self.time_table[aim_ins.id] + ins_latency)
                    
        for ins in BB1[:-1]:
            flag_inserted = False
            lowest_time = lowest_time_start_loop
            if ins.local_dependencies == []:
                flag_inserted = self.insert_ASAP(ins, lowest_time)
            else:
                for (opname, id) in ins.local_dependencies:
                    aim_ins = instructions[id]
                    ins_latency = 1
                    if aim_ins.operation in self.MUL_OPS:
                        ins_latency = 3
                    lowest_time = max(lowest_time, 
                                      self.time_table[aim_ins.id] + ins_latency)
                flag_inserted = self.insert_ASAP(ins, lowest_time) 

            if not flag_inserted:
                self.append(ins, lowest_time=lowest_time)

        # 单独处理最后一个指令 loop LoopStart
        BB1[-1].loopStart = lowest_time_start_loop
        loop_ins = BB1[-1]
        # calculate the interloop dependencies latency
        time_need_after_loop = 0
        for ins in BB1:
            for (opmap) in ins.interloop_dependencies:
                aim_ins = instructions[ ins.interloop_dependencies[opmap]['BB1'] ]
                ins_latency = 1
                if aim_ins.operation in self.MUL_OPS:
                    ins_latency = 3
                
                # 从depending的指令到循环结束再到自己的运行时间
                tmp_time_afterward = (len(self.bundles) - self.time_table[aim_ins.id])
                tmp_time_before = (self.time_table[ins.id] - lowest_time_start_loop)
                tmp_time_need = ins_latency - tmp_time_afterward - tmp_time_before
                time_need_after_loop = max(time_need_after_loop, tmp_time_need)
                
        # import ipdb; ipdb.set_trace()
        flag_inserted_loop = self.insert_ASAP(BB1[-1], len(self.bundles) + time_need_after_loop - 1)
        if not flag_inserted_loop:
            self.append(BB1[-1], lowest_time=len(self.bundles) + time_need_after_loop - 1)
        
        self.time_end_of_loop = len(self.bundles) - 1
            
    def schedule_BB2(self, instructions, BB2):
        for ins in BB2:
            flag_inserted = False
            lowest_time = len(self.bundles)

            for (opname, id) in ins.loop_invariant:
                aim_ins = instructions[id]
                ins_latency = 1
                if aim_ins.operation in self.MUL_OPS:
                    ins_latency = 3
                lowest_time = max(lowest_time, 
                                  self.time_table[aim_ins.id] + ins_latency)
            for (opname, id) in ins.post_loop_dependencies:
                aim_ins = instructions[id]
                ins_latency = 1
                if aim_ins.operation in self.MUL_OPS:
                    ins_latency = 3
                lowest_time = max(lowest_time, 
                                  self.time_table[aim_ins.id] + ins_latency)
            for (opname, id) in ins.local_dependencies:
                aim_ins = instructions[id]
                ins_latency = 1
                if aim_ins.operation in self.MUL_OPS:
                    ins_latency = 3
                lowest_time = max(lowest_time, 
                                  self.time_table[aim_ins.id] + ins_latency)
                                
            flag_inserted = self.insert_ASAP(ins, lowest_time)
            if not flag_inserted:
                self.append(ins, lowest_time=lowest_time)


    def schedule_simp(self, instructions, BB0, BB1, BB2, flag_has_loop, loop_start):
        self.time_table = [None for i in range(0, len(instructions))]
        # print(self.time_table)
        self.schedule_BB0(instructions, BB0)
        # print(self.time_table)

        self.schedule_BB1(instructions, BB1)

        self.schedule_BB2(instructions, BB2)

        # for bundle in self.bundles:
        #     for ins in bundle:
        #         print(ins)
        #     print()

    def lowerboundII(self, BB1):
        count_units = [0, 0, 0, 0]
        for ins in BB1:
            if ins.operation in self.ALU_OPS:
                count_units[0] += 1
            elif ins.operation in self.MUL_OPS:
                count_units[1] += 1
            elif ins.operation in self.MEM_OPS:
                count_units[2] += 1
            elif ins.operation in self.LOOP_OPS:
                count_units[3] += 1
        count_units[0] = ceil(count_units[0] / 2)
        return max(count_units)

    def check_interloop_dependencies(self, instructions, BB1):
        ret = True
        for ins in BB1:
            for (opmap) in ins.interloop_dependencies:
                # import ipdb; ipdb.set_trace()
                aim_ins = instructions[ ins.interloop_dependencies[opmap]['BB1'] ]
                time_aim_ins = self.time_table[aim_ins.id]
                time_cur_ins = self.time_table[ins.id]
                latency = 1
                if aim_ins.operation in self.MUL_OPS:
                    latency = 3
                if time_aim_ins + latency > time_cur_ins + self.II:
                    ret = False
                    return ret
        return ret

    def schedule_pip_BB1(self, instructions, BB0, BB1):
        if len(BB1) == 0:
            self.time_start_of_loop = len(self.bundles)
            self.time_end_of_loop = len(self.bundles)
            return
        lowest_time_start_loop = len(self.bundles)
        for ins in BB1:
            for (opname, id) in ins.loop_invariant:
                aim_ins = instructions[id]
                ins_latency = 1
                if aim_ins.operation in self.MUL_OPS:
                    ins_latency = 3
                lowest_time_start_loop = max(lowest_time_start_loop, 
                                              self.time_table[aim_ins.id] + ins_latency)
            for (opmap) in ins.interloop_dependencies:
                # import ipdb; ipdb.set_trace()
                # for BBname in ins.interloop_dependencies[opmap]:
                #    print(ins.interloop_dependencies[opmap][BBname])

                if 'BB0' in ins.interloop_dependencies[opmap]:
                    aim_ins = instructions[ ins.interloop_dependencies[opmap]['BB0'] ]
                    ins_latency = 1
                    if aim_ins.operation in self.MUL_OPS:
                        ins_latency = 3
                    lowest_time_start_loop = max(lowest_time_start_loop, 
                                                  self.time_table[aim_ins.id] + ins_latency)

        self.time_start_of_loop = lowest_time_start_loop

        while True:
            flag_no_conflict = True
            # print("II = ", self.II)

            for ins in BB1[:-1]:
                flag_inserted = False
                lowest_time = lowest_time_start_loop
                if ins.local_dependencies == []:
                    flag_inserted = self.insert_ASAP_pip(ins, lowest_time)
                else:
                    for (opname, id) in ins.local_dependencies:
                        aim_ins = instructions[id]
                        ins_latency = 1
                        if aim_ins.operation in self.MUL_OPS:
                            ins_latency = 3
                        # import ipdb; ipdb.set_trace()
                        lowest_time = max(lowest_time, 
                                          self.time_table[aim_ins.id] + ins_latency)
                    flag_inserted = self.insert_ASAP_pip(ins, lowest_time) 

                if not flag_inserted:
                    self.append_pip(ins, lowest_time=lowest_time)
            
            flag_no_conflict = self.check_interloop_dependencies(instructions, BB1)

            if flag_no_conflict:
                break
            else:
                self.II += 1
                self.bundles = self.bundles[:self.time_start_of_loop]
                for i in range(len(BB0), len(BB0) + len(BB1)):
                    self.time_table[i] = None
        
        while (len(self.bundles) - self.time_start_of_loop) % self.II != 0:
            self.bundles.append([None, None, None, None, None])
            self.spread_reserved()
        
        time_to_jump = self.time_start_of_loop + self.II - 1
        new_instruction = Instruction("loop.pip " + str(self.time_start_of_loop), len(instructions))
        instructions.append(new_instruction)
        self.bundles[time_to_jump][4] = new_instruction
        

    def schedule_pip(self, instructions, BB0, BB1, BB2, flag_has_loop, loop_start):
        self.time_table = [None for i in range(0, len(instructions))]
        self.schedule_BB0(instructions, BB0)

        self.II = self.lowerboundII(BB1)
        if self.II == 0:
            self.II = 1
        # print("II = ", self.II)

        self.schedule_pip_BB1(instructions, BB0, BB1)    

        self.time_end_of_loop = len(self.bundles)

        self.schedule_BB2(instructions, BB2)

        self.predicator = [ [None for i in range(5)] for j in range(len(self.bundles)) ]

        # self.print()
    
    def print(self):
        print("II = ", self.II)
        for bundle in self.bundles:
            for ins in bundle:
                # print(ins, end="\t\t ")
                if ins is not None and ins != "--":
                    print(ins.str_new(), end="\t\t")
                else:
                    print("--", end="\t\t")
            print()
    
    def calculate_stage(self):
        cnt_stage = 0
        cnt_in_stage = 0
        for id, _ in enumerate(self.bundles[self.time_start_of_loop:self.time_end_of_loop]):
            if cnt_in_stage == 0:
                self.stages.append([])
            self.stages[cnt_stage].append(id + self.time_start_of_loop)

            cnt_in_stage += 1
            if cnt_in_stage == self.II:
                cnt_stage += 1
                cnt_in_stage = 0
    
    def print_loop(self):
        print("\n============== BB1 ==========================")
        print("start: ", self.time_start_of_loop)
        print("end: ", self.time_end_of_loop)

        for stage_id, stage in enumerate(self.stages):
            print("========================================")
            print("Stage: ", stage_id)
            for bundle_id in stage:
                bundle = self.bundles[bundle_id]
                for ins in bundle:
                    if ins is not None and ins != "--":
                        print(ins.str_new(), end="\t\t")
                    else:
                        print("--", end="\t\t")

                print()