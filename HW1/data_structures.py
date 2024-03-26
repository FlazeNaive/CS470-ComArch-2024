# data_structures.py
def initialize_processor():
    return {
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
