import json
from PrepareLoop import PrepareLoop

def generate_output_simp(instructions, bundles, output_json_simp):
    res = []
    for bundle in bundles:
        this_bundle = []
        for ins in bundle:
            if ins is not None:
                this_bundle.append(ins.str_new())
            else:
                this_bundle.append("nop")
        res.append(this_bundle)
    with open(output_json_simp, "w") as f:
        json.dump(res, f, indent=2)

def generate_output_pip(instructions, prepareloop: PrepareLoop, bundles, output_json_pip):
    res = []
    for bundle in bundles:
        this_bundle = []
        for ins in bundle:
            if ins is not None and ins != '--':
                new_str = ""
                if ins.id in range(len(prepareloop.predicators)):
                    if prepareloop.predicators[ins.id] is not None:
                        new_str += "(p{}) ".format(prepareloop.predicators[ins.id])
                new_str += ins.str_new()
                this_bundle.append(new_str)
            else:
                this_bundle.append("nop")
        res.append(this_bundle)

    with open(output_json_pip, "w") as f:
        json.dump(res, f, indent=2)
    pass