class Scheduler_simp:
    MUL_OPS = ["mulu"]
    ALU_OPS = ["add", "sub", "mov", "addi"]
    MEM_OPS = ["ld", "st"]
    LOOP_OPS = ["loop", "loop.pip"]

    NOP_OPS = ["nop"]


    def __init__(self, processor):
        self.bundles = []                        # [(ALU0, ALU1, Mult, Mem, Branch)]
        self.time_table = []                     # [id_bundle], 下表是id_instruction
        self.processor = processor

        self.time_end_of_loop = 0
    
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

    def insert_endofloop(self, ins, lowest_time=0):
        import ipdb; ipdb.set_trace()
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