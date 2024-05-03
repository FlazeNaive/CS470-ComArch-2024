def debug_print_ins(ins):
    print(ins.id, ": ", ins)
    # print("operation: ", ins.operation)
    # print("dst: ", ins.dst)
    # print("opA: ", ins.opA)
    # print("opB: ", ins.opB)
    # print("src: ", ins.src)
    # print("immediate: ", ins.immediate)
    # print(ins.local_dependencies)
    print()

def debug_print_blockes(BB, name="BB"):
    print("========================================")
    print("====="+name+"=====")
    for ins in BB:
        debug_print_ins(ins)