from InParser import parse_input
from Processor import Processor
from Scheduler import Scheduler
from RegAlloc import RegisterAllocator
from OutGenerator import generate_output_simp, generate_output_pip

def main(input_json, output_json_simp, output_json_pip):
    instructions = parse_input(input_json)
    processor = Processor()
    scheduler = Scheduler(processor)
    allocator = RegisterAllocator(processor)

    for ins in instructions:
        print(ins)
        print("dst: ", ins.dst)
        print("opA: ", ins.op)
        print("opB: ", ins.op)
        print()
        print("src: ", ins.src)
        print("immediate: ", ins.immediate)
    
    scheduler.schedule_instructions(instructions)
    allocator.allocate_registers(instructions)
    
    generate_output_simp(instructions, output_json_simp)
    generate_output_pip(instructions, output_json_pip)

if __name__ == "__main__":
    import sys
    input_json = sys.argv[1]
    output_json_simp = sys.argv[2]
    output_json_pip = sys.argv[3]
    main(input_json, output_json_simp, output_json_pip)