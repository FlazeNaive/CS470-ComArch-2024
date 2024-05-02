import json
from Instruction import Instruction

def parse_input(input_json):
    with open(input_json, 'r') as file:
        data = json.load(file)
    return [Instruction(line) for line in data]