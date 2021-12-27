import os
import sys
import astor
import json
from ast import parse
from ast_instrumenter.ASTInstrumenterConsumptionTracker import ASTInstrumenterConsumptionTracker


# Generate frame['heapAlloc']['total'] to frame records for pie chart.
def sumVars(frame):
    # Recursively calls for frame's children.
    for child in frame['children']:
        sumVars(child)

    # Handle the summary of vars.
    total_memory = 0
    typed_memory = []
    raw_typed_memory = {}
    for var in frame['heapAlloc']['vars']:
        var_type = var['type']
        var_value = var['value']
        total_memory += var_value
        if var_type in raw_typed_memory:
            raw_typed_memory[var_type] += var_value
        else:
            raw_typed_memory[var_type] = var_value
    for entry in sorted(raw_typed_memory.items(), key=lambda x: x[1], reverse=True):
        typed_memory.append({
            'type': entry[0],
            'value': entry[1]
        })
    frame['heapAlloc']['total'] = {
        'total_memory': total_memory,
        'typed_memory': typed_memory
    }


def run(file_path):
    f = open(file_path)
    initial_source = f.read()
    f.close()

    print('-------------------- initial source --------------------')
    f = open("data/initial_source.py", "w")
    f.write(initial_source)
    f.close()

    print('-------------------- initial ast --------------------')
    initial_ast = parse(initial_source)
    f = open("data/initial_ast.txt", "w")
    f.write(astor.dump_tree(initial_ast))
    f.close()

    print('-------------------- instrumented ast --------------------')
    instrumented_ast = ASTInstrumenterConsumptionTracker().visit(initial_ast)
    f = open("data/instrumented_ast.txt", "w")
    f.write(astor.dump_tree(instrumented_ast))
    f.close()

    print('-------------------- instrumented source --------------------')
    instrumented_source = astor.to_source(instrumented_ast)
    f = open("data/instrumented_source.py", "w")
    f.write(instrumented_source)
    f.close()

    print('-------------------- Run program --------------------')
    code = compile(instrumented_source, filename='', mode='exec')
    env = {}
    exec(code, env)

    print('-------------------- Generate stacks.json --------------------')
    stacks = env['root_frame_reference']
    sumVars(stacks)
    f = open("data/stacks.json", "w")
    f.write(json.dumps(stacks, indent=4, sort_keys=True))
    f.close()

    print('-------------------- Display flame graph and pie chart based on stacks.json --------------------')
    f = open("../my-app/src/data/stacks.json", "w")
    f.write(json.dumps(stacks, indent=4, sort_keys=True))
    f.close()
    os.system("cd ../my-app && npm run start")


if __name__ == '__main__':
    print("\nMake sure that the initial source code must have a main function and run from it as an entry.")
    while True:
        cmd = input("PyProfile> ").split(' ')
        if cmd[0] == 'quit':
            break
        elif len(cmd) == 2 and cmd[0] == 'profile':
            run(str(cmd[1]))
        else:
            print("Invalid Command!", file=sys.stderr)
            continue
