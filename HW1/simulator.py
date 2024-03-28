# simulator.py
from data_structures import ActiveListEntry, IntegerQueueEntry, compare_json
from instruction import decode_instruction

import json

class Simulator:
    def __init__(self):
        self.instructions = []
        self.parsedInstructions = []
        self.logs = []
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

    def append_logs(self):
        self.logs.append(json.loads(json.dumps(self.processor_state)))

    def run(self):
        self.append_logs()
        while self.processor_state['PC'] < len(self.instructions):
            # 逐条处理指令，每个cycle fetch 4 instructions
            to_fetch = min(4, len(self.instructions) - self.processor_state['PC'] - 1)
            for i in range(to_fetch):
                # Only for test
                print("[INFO] fetching: ", self.processor_state['PC'])
                self.processor_state['DecodedPCs'].append(self.processor_state['PC'])
                self.processor_state['PC'] += 1
            
            for 
                        
            self.append_logs()
            # import ipdb; ipdb.set_trace()
            # cycle 0, 1是对的
            


    def print_state(self):
        print(json.dumps(self.processor_state, indent=4))
    
    def debug_check_same(self, std_state):
        mystate = json.loads(json.dumps(self.processor_state))
        # check if two json are the same
        if mystate == std_state:
            print("两个JSON对象相同")
        else:
            compare_json(mystate, std_state)