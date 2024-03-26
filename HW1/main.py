# 初始化数据结构
PC = 0
PhysicalRegisterFile = [0] * 64
DecodedInstructions = []
ExceptionFlag = False
ExceptionPC = 0
RegisterMapTable = list(range(32))  # x0到x31映射到p0到p31
FreeList = list(range(32, 64))  # p32到p63作为空闲列表初始值
BusyBitTable = [False] * 64
ActiveList = []
IntegerQueue = []

