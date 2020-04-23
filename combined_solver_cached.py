from graphsolver import GraphSolver
from graphsolver import weight
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
from simple_tests import test6
from optimizer import optimize
# import opt_sorted_central_avg
# import optimized_solver_1
# import optimized_solver_1_sorted
# import optimized_solver_1_sorted_allPaths
# import opt_sorted_central_only
# import opt_sorted_central_basic

from importlib import import_module
import json
from os.path import join
import os
from parse import write_output_file
from time import time

isDeterministic = False

def solve(G):
    PREV_OUTPUTS_FILENAME = join(OUTPUT_DIRECTORY, 'all_prev_outputs.txt')

    solvers = [
        'opt_sorted_central_avg',
        'optimized_solver_1',
        'optimized_solver_1_sorted',
        'optimized_solver_1_sorted_allPaths',
        'opt_sorted_central_only',
        'opt_sorted_central_basic'
    ]

    quit_on_0_cost = ['opt_sorted_central_avg']

    global all_prev_outputs
    # Don't want to load the json every time solve() is called
    if os.path.isfile(PREV_OUTPUTS_FILENAME):
        with open(PREV_OUTPUTS_FILENAME, 'r') as f:
            all_prev_outputs = json.load(f)
    else:
        # Key: input filename
        # Value: {best: solver_filename, data: {solver_filename: {cost: x, time: x}}
        all_prev_outputs = {}

    all_trees = []
    prev_outputs = all_prev_outputs.get(input_filename, {'best': None, 'data': {}})
    if prev_outputs['best'] is None:
        # Hasn't been run before
        all_prev_outputs[input_filename] = prev_outputs

    for solver_filename in solvers:
        mod = import_module(solver_filename)

        if getattr(mod, 'isDeterministic', False) and solver_filename in prev_outputs['data'].keys():
            print('{} skipped computation because it is deterministic and was run before'.format(solver_filename))

            cost = prev_outputs['data'][solver_filename]['cost']
            runtime = prev_outputs['data'][solver_filename]['runtime']

            print(solver_filename, 'Average cost: ', cost)
            print(solver_filename, 'completed in time:', runtime)
            continue

        start = time()
        tree = mod.solve(G)
        end = time()
        cost = average_pairwise_distance(tree)
        all_trees.append(tree)

        out_file = os.path.join(OUTPUT_DIRECTORY, input_filename[:-3], solver_filename + '.out')
        if not os.path.isfile(out_file) or solver_filename not in prev_outputs['data'].keys() \
                or prev_outputs['data'][solver_filename]['cost'] > cost:
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            write_output_file(tree, out_file)

            prev_outputs['data'][solver_filename] = {'cost': cost, 'runtime': end-start}
            if prev_outputs['best'] is None or cost < prev_outputs['data'][prev_outputs['best']]['cost']:
                prev_outputs['best'] = solver_filename
                print('New best solver for {} is {} with cost {} and time {}' \
                        .format(input_filename, solver_filename, cost, end-start))

        if solver_filename in quit_on_0_cost and average_pairwise_distance(tree) == 0:
            close()
            return tree

    close()
    all_trees.sort(key=lambda t: average_pairwise_distance(t))
    return all_trees[0]

def close():
    PREV_OUTPUTS_FILENAME = join(OUTPUT_DIRECTORY, 'all_prev_outputs.txt')
    with open(PREV_OUTPUTS_FILENAME, 'w') as f:
        json.dump(all_prev_outputs, f, indent=2)

# test6(solve)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')
