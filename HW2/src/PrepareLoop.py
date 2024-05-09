from Scheduler import Scheduler
from Instruction import Instruction

class PrepareLoop:
    def __init__(self, processor):
        self.processor = processor
        self.predicators = []
        self.pred_base = 32
    
    def print_pred(self, scheduler: Scheduler):
        for stage_id, stage in enumerate(scheduler.stages):
            for bundle_id in stage:
                for ins in scheduler.bundles[bundle_id]:
                    if ins is not None and ins != "--":
                        if ins.operation != "loop.pip":
                            print("(p{})".format(self.predicators[ins.id]), end="")
                        print(ins.str_new(), end="\t\t")
                    else:
                        print("--", end="\t\t")
                print("")
    
    def zip_stage(self, scheduler: Scheduler):
        start_loop = scheduler.time_start_of_loop
        end_loop = scheduler.time_end_of_loop

        for bundle_id in range(start_loop, end_loop):
            that_id = bundle_id + scheduler.II
            while (that_id < end_loop):
                for slot in range(5):
                    if scheduler.bundles[bundle_id][slot] == '--':
                        if scheduler.bundles[that_id][slot] is not None and scheduler.bundles[that_id][slot] != '--':
                            scheduler.bundles[bundle_id][slot] = scheduler.bundles[that_id][slot]
                that_id += scheduler.II
        
        for bundle_id in reversed(range(start_loop + scheduler.II, end_loop)):
            scheduler.bundles.pop(bundle_id)
        

    def prepare(self, instructions, scheduler: Scheduler):
        self.predicators = [None for i in range(len(instructions) + 1)]
        # print(instructions[-1])
        # print(":!!!!")

        scheduler.calculate_stage()
        # scheduler.print_loop()

        num_stage = len(scheduler.stages)
        new_mov1 = Instruction("mov p32, true", len(instructions))
        new_mov_EC = Instruction("mov EC, {}".format(num_stage - 1), len(instructions) + 1)

        # for ins in instructions:
        #     print(ins)
        # print("LOOP INSTRUCTION: ", scheduler.bundles[scheduler.time_start_of_loop + scheduler.II - 1][4])
        # for bundle in scheduler.bundles:
        #     for ins in bundle:
        #         print(ins)
        # scheduler.bundles[scheduler.time_start_of_loop + scheduler.II - 1][4].loopStart = scheduler.time_start_of_loop

        for stage_id, stage in enumerate(scheduler.stages):
            for bundle_id in stage:
                for ins in scheduler.bundles[bundle_id]:
                    if ins is not None and ins != '--' and ins.operation != "loop.pip":
                        self.predicators[ins.id] = self.pred_base + stage_id

        # self.print_pred(scheduler)


        self.zip_stage(scheduler)
        # scheduler.print()
        # self.print_pred(scheduler)

        
        scheduler.insert_prepareLoop(new_mov_EC)
        scheduler.insert_prepareLoop(new_mov1)
        # for ins in instructions:
        #     if ins.operation == 'loop.pip':
        #         ins.loopStart = scheduler.time_start_of_loop

        # scheduler.print()


        pass
    pass