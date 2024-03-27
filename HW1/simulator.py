# simulator.py
from data_structures import initialize_processor
from instruction import decode_instruction

import json

class Simulator:
    def __init__(self):
        self.instructions = []
        self.processor_state = {
            "PC": 0,
            "PhysicalRegisterFile": [0] * 64,
            "DecodedInstructions": [],
            "ExceptionFlag": False,
            "ExceptionPC": 0,
            "RegisterMapTable": list(range(32)),
            "FreeList": list(range(32, 64)),
            "BusyBitTable": [False] * 64,
            "ActiveList": [],
            "IntegerQueue": [],
            "halt": False  # 控制模拟器是否停止
        }

    def load_instructions(self, input_file_path):
        # 读取指令集文件并存储
        # load instructions from json file
        self.instructions = json.load(open(input_file_path))


    def run(self):
        # Only for test
        for ins in self.instructions:
            opcode, operands = decode_instruction(ins)
            print(opcode, operands)
            self.processor_state["DecodedInstructions"].append((opcode, operands))
        print("[INFO] Instructions loaded")

    def print_state(self):
        # 输出处理器的当前状态
        print(self.processor_state)
