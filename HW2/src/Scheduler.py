class Scheduler_simp:
    MUL_OPS = ["mulu"]
    ALU_OPS = ["add", "sub", "mov", "addi"]
    MEM_OPS = ["ld", "st"]
    LOOP_OPS = ["loop", "loop.pip"]

    NOP_OPS = ["nop"]


    def __init__(self, processor):
        self.bundles = []                        # [(ALU0, ALU1, Mult, Mem, Branch)]
        self.time_table = []                     # [(id_instruction, id_bundle)]
        self.processor = processor
    
    def insert_ASAP_BB0(self, BB0, ins, id_low):
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

    def append_BB0(self, BB0, ins, lowest_time=0):
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
                flag_inserted = self.insert_ASAP_BB0(BB0, ins, 0)
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
                flag_inserted = self.insert_ASAP_BB0(BB0, ins, lowest_time) 

            if not flag_inserted:
                self.append_BB0(BB0, ins, lowest_time=lowest_time)


    def schedule_simp(self, instructions, BB0, BB1, BB2, flag_has_loop, loop_start):
        self.time_table = [None for i in range(0, len(instructions))]
        # print(self.time_table)
        self.schedule_BB0(instructions, BB0)
        # print(self.time_table)
        for bundle in self.bundles:
            for ins in bundle:
                print(ins)
            print()