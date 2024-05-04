def debug_print_ins(ins):
    print(ins.id, ": ", ins)
    # print("operation: ", ins.operation)
    # print("dst: ", ins.dst)
    # print("opA: ", ins.opA)
    # print("opB: ", ins.opB)
    # print("src: ", ins.src)
    # print("immediate: ", ins.immediate)
    # print("dst_new: ", ins.dst_new)
    # print("opA_new: ", ins.opA_new)
    # print("opB_new: ", ins.opB_new)
    # print("src_new: ", ins.src_new)

    print("local_dependencies: ")
    print(ins.local_dependencies)
    print("interloop_dependencies: ")
    print(ins.interloop_dependencies)
    print("post_loop_dependencies: ")
    print(ins.post_loop_dependencies)
    print("loop_invariant: ")
    print(ins.loop_invariant)

    print()

def debug_print_blockes(BB, name="BB"):
    print("========================================")
    print("====="+name+"=====")
    for ins in BB:
        debug_print_ins(ins)