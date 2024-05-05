from InParser import parse_input, parse_blockes

from Processor import Processor
from Dependencies import calculate_dependencies
from Scheduler import Scheduler

from RegAlloc import RegisterAllocator_simp, RegisterAllocator_pip

from Instruction import CONST_NOP
from utils import debug_print_ins, debug_print_blockes
from OutGenerator import generate_output_simp, generate_output_pip

import copy

def main(input_json, output_json_simp, output_json_pip):
    instructions = parse_input(input_json)
    processor = Processor()
    allocator_simp = RegisterAllocator_simp(processor)
    allocator_pip = RegisterAllocator_pip(processor)
    schedule_simp_class = Scheduler(processor)
    schedule_pip_class = Scheduler(processor)

    BB0, BB1, BB2, flag_has_loop, loop_start = parse_blockes(instructions)

    
    # print("========================================")
    # print("======= LOADED and PARSED =======")
    # print("========================================")
    
    calculate_dependencies(BB0, BB1, BB2)

    # back_up_BBs = [copy.deepcopy(BB0), copy.deepcopy(BB1), copy.deepcopy(BB2)]
    back_up_instructions = copy.deepcopy(instructions)

    # debug_print_blockes(BB0, "BB0")
    # debug_print_blockes(BB1, "BB1")
    # debug_print_blockes(BB2, "BB2")


    print("========================================")
    print("======= DEPENDENCIES DONE =======")
    print("========================================")

    schedule_simp_class.schedule_simp(instructions, BB0, BB1, BB2, flag_has_loop, loop_start)
    allocator_simp.allocate_registers(instructions, schedule_simp_class)

    # debug_print_blockes(instructions, "Instructions")

    generate_output_simp(instructions, schedule_simp_class.bundles, output_json_simp)

    print("========================================")
    print("======= Schedule Simple =======")
    print("========================================")

    BB0, BB1, BB2, flag_has_loop, loop_start = parse_blockes(back_up_instructions)
    # BB0, BB1, BB2 = back_up_BBs
    # instructions = back_up_instructions

    schedule_pip_class.schedule_pip(back_up_instructions, BB0, BB1, BB2, flag_has_loop, loop_start)
    allocator_pip.allocate_registers(back_up_instructions, schedule_pip_class, BB0, BB1, BB2)

    # debug_print_blockes(instructions, "Instructions")
    
    generate_output_pip(instructions, schedule_pip_class.bundles, output_json_pip)

if __name__ == "__main__":
    import sys
    input_json = sys.argv[1]
    output_json_simp = sys.argv[2]
    output_json_pip = sys.argv[3]
    main(input_json, output_json_simp, output_json_pip)