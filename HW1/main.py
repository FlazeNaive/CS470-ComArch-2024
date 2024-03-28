# main.py
import sys
import json
from simulator import Simulator

if __name__ == "__main__":
    input_file = "test/given_tests/01/input.json"  # 根据需要调整路径
    std_out = "test/given_tests/01/output.json"  # 根据需要调整路径
    simulator = Simulator()
    simulator.load_instructions(input_file)
    simulator.run()
    simulator.print_state()

    std_out_json = json.loads(open(std_out).read())
    # print(std_out_json[0])
    simulator.debug_check_same(std_out_json[0])