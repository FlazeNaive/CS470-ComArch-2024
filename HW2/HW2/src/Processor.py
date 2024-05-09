class Processor:
    def __init__(self):
        self.registers = [0] * 96  # Example for general-purpose registers
        self.pipeline = []

    def reset_pipeline(self):
        self.pipeline = []