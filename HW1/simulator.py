# simulator.py
from data_structures import initialize_processor
from instruction import decode_instruction

class Simulator:
    def __init__(self):
        self.processor_state = initialize_processor()

    def load_instructions(self, input_file):
        # 读取指令集文件并存储
        pass

    def run(self):
        # 主循环，按周期更新处理器状态
        while not self.processor_state["halt"]:
            # 例如，获取、解码、执行指令等
            decode_instruction(self.processor_state)
            # 更新状态等
            self.processor_state["PC"] += 1  # 示例

    def print_state(self):
        # 输出处理器的当前状态
        print(self.processor_state)
