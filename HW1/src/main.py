# main.py
import sys
import json
from simulator import Simulator

def main(input_file, output_file):
    input_file = "test/given_tests/01/input.json"  # 
    std_out = "test/given_tests/01/output.json"  # 
    simulator = Simulator()
    simulator.load_instructions(input_file)
    simulator.run()
    simulator.print_state()

    std_out_json = json.loads(open(std_out).read())

    # INFO: only for debug
    # print(std_out_json[0])
    # simulator.debug_check_same(std_out_json[0])

if __name__ == "__main__":
    import sys
    input_json = sys.argv[1]
    output_json_simp = sys.argv[2]
    output_json_pip = sys.argv[3]
    main(input_json, output_json_simp, output_json_pip)
