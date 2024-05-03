class Scheduler:
    def __init__(self, processor):
        self.processor = processor
    
    def schedule_instructions(self, instructions):
        # Implement ASAP or other scheduling algorithms here
        pass

    def calculate_ii(self, instructions):
        # Calculate initiation interval based on dependencies and processor resources
        return max(1, min(len(instructions), self.processor.num_ALUs))

def calculate_local_dependencies(BB):
    # only consider the last instruction that 
    #                 writes to our src/opA/opB

    for i in range(len(BB) - 1, -1, -1):
        opNeed = set()
        if BB[i].opA is not None:
            opNeed.add(BB[i].opA)
        if BB[i].opB is not None:
            opNeed.add(BB[i].opB)
        if BB[i].src is not None:
            opNeed.add(BB[i].src)

        for j in range(i - 1, -1, -1):
            if BB[j].dst in opNeed:
                BB[i].local_dependencies.append(BB[j].id)
                opNeed.remove(BB[j].dst)
            if opNeed == set():
                break



def calculate_dependencies(BB0, BB1, BB2):
    # calculate dependencies:
    #     local dependencies, interloop dependencies, post-loop dependencies
    #                         BB0/BB1 -> BB1             BB1 -> BB2


    # local dependencies
    calculate_local_dependencies(BB0)
    calculate_local_dependencies(BB1)
    calculate_local_dependencies(BB2)

    # TODO: interloop dependencies

    # TODO: post-loop dependencies