
def calculate_local_dependencies(BB):
    # only consider the last instruction that 
    #                 writes to our src/opA/opB

    for i in range(len(BB) - 1, -1, -1):
        opNeed_set = set()
        opNeed = []
        if BB[i].opA is not None:
            opNeed_set.add(BB[i].opA)
            opNeed.append((BB[i].opA, 'opA'))
        if BB[i].opB is not None:
            opNeed_set.add(BB[i].opB)
            opNeed.append((BB[i].opB, 'opB'))
        if BB[i].src is not None:
            opNeed_set.add(BB[i].src)
            opNeed.append((BB[i].src, 'src'))
        if BB[i].addr is not None:
            opNeed_set.add(BB[i].addr)
            opNeed.append((BB[i].addr, 'addr'))

        # import ipdb; ipdb.set_trace()
        for j in range(i - 1, -1, -1):
            # print(opNeed_set)
            for (key, opname) in opNeed:
                if key == BB[j].dst and BB[j].dst in opNeed_set:
                    BB[i].local_dependencies.append((opname, BB[j].id))
            if BB[j].dst in opNeed_set:
                opNeed_set.remove(BB[j].dst)
            if opNeed_set == set():
                break

def interloop_dependencies_clean(BB, i, opname):
    print(BB[i])
    # import ipdb; ipdb.set_trace()
    if BB[i].interloop_dependencies.get(opname) is not None:
        # import ipdb; ipdb.set_trace()
        if BB[i].interloop_dependencies[opname] == {}:
            # no opA dependency
            del BB[i].interloop_dependencies[opname]
        elif any( xx[0] == opname for xx in BB[i].local_dependencies):
            del BB[i].interloop_dependencies[opname]
        elif BB[i].interloop_dependencies[opname].get('BB0') is not None and BB[i].interloop_dependencies[opname].get('BB1') is None:
            # import ipdb; ipdb.set_trace()
            # opA only depends on BB0
            BB[i].loop_invariant.append((opname, BB[i].interloop_dependencies[opname]['BB0']))
            del BB[i].interloop_dependencies[opname]
        else:
            for (op_local, _) in BB[i].local_dependencies:
                if op_local == opname:
                    del BB[i].interloop_dependencies[opname]
    
def calculate_interloop_dependencies(BB0, BB1):
    for i in range(len(BB1)):
        op_need_set = set()
        op_need = []
        if BB1[i].opA is not None:
            op_need_set.add(BB1[i].opA)
            op_need.append((BB1[i].opA, 'opA'))
            BB1[i].interloop_dependencies['opA'] = {}
        if BB1[i].opB is not None:
            op_need_set.add(BB1[i].opB)
            op_need.append((BB1[i].opB, 'opB'))
            BB1[i].interloop_dependencies['opB'] = {}
        if BB1[i].src is not None:
            op_need_set.add(BB1[i].src)
            op_need.append((BB1[i].src, 'src'))
            BB1[i].interloop_dependencies['src'] = {}
        if BB1[i].addr is not None:
            op_need_set.add(BB1[i].addr)
            op_need.append((BB1[i].addr, 'addr'))
            BB1[i].interloop_dependencies['addr'] = {}
        
        for j in range(len(BB0) - 1, -1, -1):
            for (key, opname) in op_need:
                if key == BB0[j].dst and BB0[j].dst in op_need_set:
                    BB1[i].interloop_dependencies[opname]['BB0'] = BB0[j].id
            if BB0[j].dst in op_need_set:
                op_need_set.remove(BB0[j].dst)
            if op_need_set == set():
                break

        op_need_set = set()
        op_need = []
        if BB1[i].opA is not None:
            op_need_set.add(BB1[i].opA)
            op_need.append((BB1[i].opA, 'opA'))
        if BB1[i].opB is not None:
            op_need_set.add(BB1[i].opB)
            op_need.append((BB1[i].opB, 'opB'))
        if BB1[i].src is not None:
            op_need_set.add(BB1[i].src)
            op_need.append((BB1[i].src, 'src'))
        if BB1[i].addr is not None:
            op_need_set.add(BB1[i].addr)
            op_need.append((BB1[i].addr, 'addr'))
        
        for j in range(len(BB1) - 1, i - 1, -1):
            # print(op_need)
            # print(BB1[j])
            # import ipdb; ipdb.set_trace()
            for (key, opname) in op_need:
                if key == BB1[j].dst and BB1[j].dst in op_need_set:
                    BB1[i].interloop_dependencies[opname]['BB1'] = BB1[j].id
            if BB1[j].dst in op_need_set:
                op_need_set.remove(BB1[j].dst)
            if op_need_set == set():
                break

        interloop_dependencies_clean(BB1, i, 'opA')
        interloop_dependencies_clean(BB1, i, 'opB')
        interloop_dependencies_clean(BB1, i, 'src')
        interloop_dependencies_clean(BB1, i, 'addr')
        
        
def calculate_loop_invariant(BB0, BB1, BB2):
    for i in range(len(BB2)):
        opNeed_set = set()
        opNeed = []
        if BB2[i].opA is not None:
            flag_not_added = True
            for (opname, id) in BB2[i].local_dependencies:
                if opname == 'opA':
                    flag_not_added = False
            if flag_not_added:
                opNeed_set.add(BB2[i].opA)
                opNeed.append((BB2[i].opA, 'opA'))
        if BB2[i].opB is not None:
            flag_not_added = True
            for (opname, id) in BB2[i].local_dependencies:
                if opname == 'opB':
                    flag_not_added = False
            if flag_not_added:
                opNeed_set.add(BB2[i].opB)
                opNeed.append((BB2[i].opB, 'opB'))
        if BB2[i].src is not None:
            flag_not_added = True
            for (opname, id) in BB2[i].local_dependencies:
                if opname == 'src':
                    flag_not_added = False
            if flag_not_added:
                opNeed_set.add(BB2[i].src)
                opNeed.append((BB2[i].src, 'src'))
        if BB2[i].addr is not None:
            flag_not_added = True
            for (opname, id) in BB2[i].local_dependencies:
                if opname == 'addr':
                    flag_not_added = False
            if flag_not_added:
                opNeed_set.add(BB2[i].addr)
                opNeed.append((BB2[i].addr, 'addr'))

        for j in range(len(BB1) - 1, -1, -1):
            for (key, opname) in opNeed:
                if key == BB1[j].dst and BB1[j].dst in opNeed_set:
                    BB2[i].post_loop_dependencies.append((opname, BB1[j].id))
            if BB1[j].dst in opNeed_set:
                opNeed_set.remove(BB1[j].dst)
            if opNeed_set == set():
                break

        for j in range(len(BB0) - 1, -1, -1):
            if opNeed_set == set():
                break
            for (key, opname) in opNeed:
                if key == BB0[j].dst and BB0[j].dst in opNeed_set:
                    BB2[i].loop_dependencies.append((opname, BB0[j].id)) 
            if BB0[j].dst in opNeed_set:
                opNeed_set.remove(BB0[j].dst)


        
        

def calculate_post_loop_dependencies(BB1, BB2):
    pass

def calculate_dependencies(BB0, BB1, BB2):
    # calculate dependencies:
    #     local dependencies, interloop dependencies, post-loop dependencies, loop invariant
    #                         BB0/BB1 -> BB1             BB1 -> BB2           BB0 -> BB1/BB2


    # local dependencies
    calculate_local_dependencies(BB0)
    calculate_local_dependencies(BB1)
    calculate_local_dependencies(BB2)

    # interloop dependencies and loop invariant in BB1
    calculate_interloop_dependencies(BB0, BB1)

    # loop invariant & post-loop dependencies in BB2
    calculate_loop_invariant(BB0, BB1, BB2)
