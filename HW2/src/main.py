from InParser import parse_input, parse_blockes

from Processor import Processor
from Dependencies import calculate_dependencies
from Scheduler import Scheduler_simp, Scheduler_pip

from RegAlloc import RegisterAllocator_simp

from Instruction import CONST_NOP
from utils import debug_print_ins, debug_print_blockes
from OutGenerator import generate_output_simp, generate_output_pip

def main(input_json, output_json_simp, output_json_pip):
    instructions = parse_input(input_json)
    processor = Processor()
    allocator = RegisterAllocator_simp(processor)
    schedule_simp_class = Scheduler_simp(processor)
    schedule_pip_class = Scheduler_pip(processor)

    BB0, BB1, BB2, flag_has_loop, loop_start = parse_blockes(instructions)

    
    # print("========================================")
    # print("======= LOADED and PARSED =======")
    # print("========================================")
    
    calculate_dependencies(BB0, BB1, BB2)

    # debug_print_blockes(BB0, "BB0")
    # debug_print_blockes(BB1, "BB1")
    # debug_print_blockes(BB2, "BB2")

    debug_print_blockes(instructions, "Instructions")

    print("========================================")
    print("======= DEPENDENCIES DONE =======")
    print("========================================")
    schedule_simp_class.schedule_simp(instructions, BB0, BB1, BB2, flag_has_loop, loop_start)

    print("========================================")
    print("======= Schedule =======")
    print("========================================")

    allocator.allocate_registers(instructions, schedule_simp_class)
    # debug_print_blockes(instructions, "Instructions")
    
    print("========================================")

    generate_output_simp(instructions, schedule_simp_class.bundles, output_json_simp)
    generate_output_pip(instructions, output_json_pip)

if __name__ == "__main__":
    import sys
    input_json = sys.argv[1]
    output_json_simp = sys.argv[2]
    output_json_pip = sys.argv[3]
    main(input_json, output_json_simp, output_json_pip)