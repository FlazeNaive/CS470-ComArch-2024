from InParser import parse_input, parse_blockes
from Processor import Processor
from Scheduler import calculate_dependencies
# from RegAlloc import RegisterAllocator
from OutGenerator import generate_output_simp, generate_output_pip
from Instruction import CONST_NOP
from utils import debug_print_ins, debug_print_blockes

def main(input_json, output_json_simp, output_json_pip):
    instructions = parse_input(input_json)
    processor = Processor()
    # scheduler = Scheduler(processor)
    # allocator = RegisterAllocator(processor)

    BB0, BB1, BB2, flag_has_loop, loop_start = parse_blockes(instructions)

    
    print("========================================")
    print("======= LOADED and PARSED =======")
    print("========================================")
    
    calculate_dependencies(BB0, BB1, BB2)

    debug_print_blockes(BB0, "BB0")
    debug_print_blockes(BB1, "BB1")
    debug_print_blockes(BB2, "BB2")


    # scheduler.schedule_instructions(instructions)
    # allocator.allocate_registers(instructions)
    
    generate_output_simp(instructions, output_json_simp)
    generate_output_pip(instructions, output_json_pip)

if __name__ == "__main__":
    import sys
    input_json = sys.argv[1]
    output_json_simp = sys.argv[2]
    output_json_pip = sys.argv[3]
    main(input_json, output_json_simp, output_json_pip)