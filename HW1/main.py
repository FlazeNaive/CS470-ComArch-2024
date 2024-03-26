# main.py
import sys
from simulator import Simulator

def main():
    input_file = "test/given_tests/01/input.json"  # 根据需要调整路径
    simulator = Simulator()
    simulator.load_instructions(input_file)
    simulator.run()

if __name__ == "__main__":
    main()