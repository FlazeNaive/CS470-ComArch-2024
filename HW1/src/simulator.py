# simulator.py
from data_structures import ActiveListEntry, IntegerQueueEntry, ALUEntry, compare_json
from instruction import Instruction

import json

class Simulator:
    def __init__(self):
        self.instructions = []
        self.parsedInstructions = []
        self.logs = []
        self.actlist = []
        self.intqueue = []
        
        # ALU_N的意思是是在ALU里呆了N个cycle
        # ALU 有2个cycle的延迟
        # 有4个ALU
        self.ALU0 = []
        self.ALU1 = []
        self.ALU2 = []  
        self.forwarding = []  # element: (physical register, value)

        self.processor_state = {
            "PC": 0,
            "PhysicalRegisterFile": [0] * 64,
            "DecodedPCs": [],           
            "ExceptionPC": 0,
            "Exception": False,
            "RegisterMapTable": list(range(32)),
            "FreeList": list(range(32, 64)),
            "BusyBitTable": [False] * 64,
            "ActiveList": [],           # max 32 entries
            "IntegerQueue": []          # max 32 entries
            #, "halt": False  # 控制模拟器是否停止
        }

    def load_instructions(self, input_file_path):
        # 读取指令集文件并存储
        # load instructions from json file
        self.instructions = json.load(open(input_file_path))
        for ins in self.instructions:
            new_instruction = Instruction(ins)
            self.parsedInstructions.append(new_instruction)

        # Only for test
        print("[INFO] Instructions loaded")

    def append_logs(self):
        # import ipdb; ipdb.set_trace()
        self.logs.append(json.loads(json.dumps(self.processor_state)))
    
    def handle_backpressure(self):
        pass


    def Fetch_and_Decode(self, flag_backpressure, flag_exception):
        to_fetch = min(4, len(self.instructions) - self.processor_state['PC'])
        if flag_backpressure:
            to_fetch = 0
        if flag_exception:
            # handle exception
            self.processor_state['PC'] = '0x10000'
            return
        for _ in range(to_fetch):
            # ========== debug output ==========
            print("[INFO] fetching: ", self.processor_state['PC'])
            self.processor_state['DecodedPCs'].append(self.processor_state['PC'])
            self.processor_state['PC'] += 1

    def Rename_and_Dispatch(self, flag_backpressure):
        # check if enough entries in 
        ## "Active List", 
        need_to_dispatch = min(4, len(self.processor_state['DecodedPCs']))
        remain_active_list = 32 - len(self.processor_state['ActiveList'])
        if remain_active_list < need_to_dispatch:
            flag_backpressure = True

        ## "Physical Registers", 姑且假设是busytable里的False数量
        remain_physical_register = self.processor_state['BusyBitTable'].count(False)
        if remain_physical_register < need_to_dispatch:
            flag_backpressure = True

        ## and "Integer Queue"
        remain_integer_queue = 32 - len(self.processor_state['IntegerQueue'])
        if remain_integer_queue < need_to_dispatch:
            flag_backpressure = True

        if not flag_backpressure:
            for ins_id in self.processor_state['DecodedPCs']:
                # rename the instruction
                cur_ins: Instruction = self.parsedInstructions[ins_id]
                logical_dest = cur_ins.dest

                # update RegMapTable, and Free List
                old_physical_dest = self.processor_state['RegisterMapTable'][logical_dest]
                new_physical_dest = self.processor_state['FreeList'].pop(0)
                self.processor_state['RegisterMapTable'][logical_dest] = new_physical_dest

                # update ActiveList
                cur_actlist = ActiveListEntry(
                        LogicalDestination=logical_dest, 
                        OldDestination=old_physical_dest, 
                        PC=ins_id)
                self.actlist.append(cur_actlist)
                # self.processor_state['ActiveList'].append(
                #     json.loads(
                #         json.dumps(cur_actlist.__dict__)))

                # update IntegerQueue
                OpAIsReady = False
                OpBIsReady = False
                OpARegTag = 0
                OpBRegTag = 0
                OpAValue = 0
                OpBValue = 0

                ## TODO: If OpA/OpB is calculated this cycle, make them ready
                # it should be done in the execute stage, by modifiying the OpXIsReady
                
                # TODO: not sure if the logic is correct but looks more likely than before
                logical_opA = cur_ins.opA_ori
                logical_opB = cur_ins.opB_ori
                physical_opA = self.processor_state["RegisterMapTable"][logical_opA]
                if cur_ins.opcode != 'addi':
                    physical_opB = self.processor_state["RegisterMapTable"][logical_opB]
                
                OpAIsReady = not self.processor_state['BusyBitTable'][physical_opA]
                if OpAIsReady:
                    OpAValue = self.processor_state['PhysicalRegisterFile'][physical_opA]
                else:
                    OpARegTag = physical_opA
                    for forward in self.forwarding:
                        if forward[0] == physical_opA:
                            OpAIsReady = True
                            OpAValue = forward[1]
                            break

                opr = cur_ins.opcode
                if opr == 'addi':
                    opr = 'add'
                    OpBIsReady = True
                    OpBValue = cur_ins.imm
                else:
                    OpBIsReady = not self.processor_state['BusyBitTable'][physical_opB]
                    if OpBIsReady:
                        OpBValue = self.processor_state['PhysicalRegisterFile'][physical_opB]
                    else:
                        OpBRegTag = physical_opB
                        for forward in self.forwarding:
                            if forward[0] == physical_opB:
                                OpBIsReady = True
                                OpBValue = forward[1]
                                break
                    
                cur_intque = IntegerQueueEntry(DestRegister=new_physical_dest,
                                      OpAIsReady=OpAIsReady,
                                      OpARegTag=OpARegTag,
                                      OpAValue=OpAValue,
                                      OpBIsReady=OpBIsReady,
                                      OpBRegTag=OpBRegTag,
                                      OpBValue=OpBValue,
                                      OpCode=opr,
                                      PC=ins_id)
                self.intqueue.append(cur_intque)
                # self.processor_state['IntegerQueue'].append(
                #     json.loads(
                #         json.dumps(cur_intque.__dict__)))

                # update BusybitTable
                self.processor_state['BusyBitTable'][new_physical_dest] = True

            self.processor_state['DecodedPCs'] = []

            # 如果没记错这一段应该是为了输出log加上的
            self.processor_state['IntegerQueue'] = []
            for intque in self.intqueue:
                self.processor_state['IntegerQueue'].append(
                    json.loads(
                        json.dumps(intque.__dict__)))
            self.processor_state['ActiveList'] = []

            for actentry in self.actlist:
                self.processor_state['ActiveList'].append(
                        json.loads(
                            json.dumps(actentry.__dict__)))

        else: 
            # 看起来好像什么都不用做，估计就把flag_backpressure设为True
            # 然后让Fetch_and_Decode啥都不干
            self.handle_backpressure()
    
    def Issue_Stage(self):
        # ready_int: 在intqueue里找四个最老的ready的int
        ready_int = []
        for intentry in self.intqueue:
            if intentry.OpAIsReady and intentry.OpBIsReady:
                ready_int.append(intentry)
            
        ready_int = sorted(ready_int, key = lambda x: x.PC)
        
        if len(ready_int) > 4:
            ready_int = ready_int[:4]
        
        return ready_int
    
    def Execute_Stage(self, ready_int, flag_exception):
        self.ALU2 = self.ALU1
        self.ALU1 = self.ALU0
        self.ALU0 = ready_int
        for intentry in self.ALU2:
            # import ipdb; ipdb.set_trace()
            # self.processor_state["PhysicalRegisterFile"][intentry.DestRegister]
            result = 0
            match intentry.OpCode:
                case 'add': 
                    result = intentry.OpAValue + intentry.OpBValue
                case 'sub':
                    result = intentry.OpAValue - intentry.OpBValue
                case 'mulu':
                    result = intentry.OpAValue * intentry.OpBValue
                case 'divu':
                    if intentry.OpBValue == 0:
                        flag_exception = True
                    else:
                        result = intentry.OpAValue // intentry.OpBValue
                case 'remu':
                    if intentry.OpBValue == 0:
                        flag_exception = True
                    else:
                        result = intentry.OpAValue % intentry.OpBValue
            
            if not flag_exception:
                # TODO: No DestiationRegister here
                pass
                # self.ALU0.append(ALUEntry(intentry.DestinationRegister, result))
            else:
                # TODO: exception
                pass
    

    def run(self):
        self.append_logs()
        count_cycle = 1
        while self.processor_state['PC'] < len(self.instructions):
            flag_backpressure = False
            flag_exception = False

            # ==================== stage 3 ====================
            # issue, execution, forwarding pipeline

            # find 4 oldest ready ins in integerqueue
            ready_int = self.Issue_Stage()

            # calculate the result
            self.Execute_Stage(ready_int, flag_exception)
            
            # TODO: update IntegerQueue

                        

            # ==================== stage 2 ====================
            # rename and dispatch
            self.Rename_and_Dispatch(flag_backpressure)

            # ==================== stage 1 ====================
            # 每个cycle fetch 4 instructions
            # fetch and decode
            self.Fetch_and_Decode(flag_backpressure, flag_exception)
            
            # ==========
            # # Only for debugging output
            # ==========
            # debug_std_out = "given_tests/01/output.json"  # 根据需要调整路径
            # debug_std_out = json.loads(open(debug_std_out).read())[count_cycle]
            # # print(debug_std_out['IntegerQueue'])
            # print("[INFO] Debugging: cycle = ", count_cycle)
            # self.debug_check_same(debug_std_out)



            # ==========
            # # logging 
            # ==========
            
            self.forwarding = []
            count_cycle += 1
            self.append_logs()
            # cycle 0, 1是对的
            

    def dump_state(self, output_file):
        json.dump(self.processor_state, open(output_file, "w"))

    def print_state(self):
        print(json.dumps(self.processor_state, indent=4))
    
    def debug_check_same(self, std_state):
        # check if two json are the same

        mystate = json.loads(json.dumps(self.processor_state))
        # print(mystate)
        # print(std_state)

        if mystate == std_state:
            print("两个JSON对象相同")
        else:
            compare_json(mystate, std_state)