# simulator.py
from data_structures import ActiveListEntry, IntegerQueueEntry, compare_json
from instruction import decode_instruction

import json

class Simulator:
    def __init__(self):
        self.instructions = []
        self.parsedInstructions = []
        self.processor_state = {
            "PC": 0,
            "PhysicalRegisterFile": [0] * 64,
            "DecodedPCs": [],
            "ExceptionPC": 0,
            "Exception": False,
            "RegisterMapTable": list(range(32)),
            "FreeList": list(range(32, 64)),
            "BusyBitTable": [False] * 64,
            "ActiveList": [],
            "IntegerQueue": []
            #, "halt": False  # 控制模拟器是否停止
        }

    def load_instructions(self, input_file_path):
        # 读取指令集文件并存储
        # load instructions from json file
        self.instructions = json.load(open(input_file_path))
        for ins in self.instructions:
            opcode, operands = decode_instruction(ins)
            self.parsedInstructions.append((opcode, operands))

        # Only for test
        print("[INFO] Instructions loaded")


    def run(self):
        pass


    def print_state(self):
        # 输出处理器的当前状态
        # print state as json
        # to print: ActiveList, BusybitTable, DecodedPCs, 
        #           Exception, ExceptionPC, 
        #           FreeList, 
        #           IntegerQueue, PC,
        #           PhysicalRegisterFile
        #           RegisterMapTable
        print(json.dumps(self.processor_state, indent=4))
    
    def debug_check_same(self, std_state):
        mystate = json.loads(json.dumps(self.processor_state))
        # check if two json are the same
        if mystate == std_state:
            print("两个JSON对象相同")
        else:
            compare_json(mystate, std_state)