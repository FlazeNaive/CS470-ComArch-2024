class ALUEntry:
    def __init__(self, PhyAddr, Value):
        self.PhyAddr = PhyAddr
        self.Value = Value
class ActiveListEntry:
    def __init__(self, LogicalDestination=0, OldDestination=0, PC=0):
        self.Done = False
        self.Exception = False
        self.LogicalDestination = LogicalDestination
        self.OldDestination = OldDestination
        self.PC = PC
    def __repr__(self):
        return ("ActiveListEntry(Done=" + str(self.Done) + ", " 
                "Exception=" + str(self.Exception) + ", "
                "LogicalDestination=" + str(self.LogicalDestination) + ", "
                "OldDestination=" + str(self.OldDestination) + ", "
                "PC=" + str(self.PC) + ")")

class IntegerQueueEntry:
    def __init__(self, DestRegister=0, 
                        OpAIsReady=False, 
                        OpARegTag=0, 
                        OpAValue=0, 
                        OpBIsReady=False, 
                        OpBRegTag=0, 
                        OpBValue=0, 
                        OpCode="NOP", 
                        PC=0):
        self.DestRegister = DestRegister
        self.OpAIsReady = OpAIsReady
        self.OpARegTag = OpARegTag
        self.OpAValue = OpAValue
        self.OpBIsReady = OpBIsReady
        self.OpBRegTag = OpBRegTag
        self.OpBValue = OpBValue
        self.OpCode = OpCode
        self.PC = PC
    
    def __repr__(self):
        return ("IntegerQueueEntry(DestRegister=" + str(self.DestRegister) + ", " 
                "OpAIsReady=" + str(self.OpAIsReady) + ", "
                "OpARegTag=" + str(self.OpARegTag) + ", "
                "OpAValue=" + str(self.OpAValue) + ", "
                "OpBIsReady=" + str(self.OpBIsReady) + ", "
                "OpBRegTag=" + str(self.OpBRegTag) + ", "
                "OpBValue=" + str(self.OpBValue) + ", "
                "OpCode='" + self.OpCode + "', "
                "PC=" + str(self.PC) + ")")

                
                
                
def compare_json(obj1, obj2, path=""):
    """递归比较两个JSON对象，并打印不同之处。"""
    # print("isdict ojb1: ", isinstance(obj1, dict))
    # print("isdict ojb2: ", isinstance(obj2, dict))
    # print("islist ojb1: ", isinstance(obj1, list))
    # print("islist ojb2: ", isinstance(obj2, list))

    if isinstance(obj1, dict) and isinstance(obj2, dict):
        for key in obj1:
            if key not in obj2:
                print(f"{path}.{key} 在std的JSON中不存在")
            else:
                compare_json(obj1[key], obj2[key], f"{path}.{key}")
        for key in obj2:
            if key not in obj1:
                print(f"{path}.{key} 在我的JSON中不存在")
    elif isinstance(obj1, list) and isinstance(obj2, list):
        for i, item in enumerate(obj1):
            if i >= len(obj2):
                print(f"{path}[{i}] 在std的JSON中不存在")
            else:
                compare_json(item, obj2[i], f"{path}[{i}]")
        for i in range(len(obj1), len(obj2)):
            print(f"{path}[{i}] 在我的JSON中不存在")
    else:
        if obj1 != obj2:
            print(f"{path} 不同: {obj1} != {obj2}")