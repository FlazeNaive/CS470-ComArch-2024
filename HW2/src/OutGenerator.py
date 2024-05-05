import json
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

def generate_output_pip(instructions, output_json_pip):
    res = []
    with open(output_json_pip, "w") as f:
        json.dump(res, f, indent=2)
    pass