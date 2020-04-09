"""
Runs all solvers in solvers.txt on all graphs in specified directory (inputs\25),
writing the outputs to corresponding entries in specified directory (outputs\25).

Usage: python runner.py inputs\25 outputs\25
"""

import os
import sys
from importlib import import_module
from time import time
from graph import weight

from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance

if __name__ == '__main__':
    assert len(sys.argv) == 3
    SOLVERS_FILENAME = 'solvers.txt'
    INPUT_DIRECTORY = sys.argv[1]
    OUTPUT_DIRECTORY = sys.argv[2]

    MAX_SIZE = 100

    with open(SOLVERS_FILENAME, 'r') as f:
        solvers = f.read().splitlines()

    input_filenames = os.listdir(INPUT_DIRECTORY)

    # for each graph
    for input_filename in input_filenames:
        # for each solver
        for solver_filename in solvers:

            # get the solver from module name
            mod = import_module(solver_filename)
            solve = getattr(mod, 'solve')

            times = []
            input_path = os.path.join(INPUT_DIRECTORY, input_filename)
            graph = read_input_file(input_path, MAX_SIZE)
            start = time()
            tree = solve(graph)
            end = time()
            times.append(end - start)
            # check if the output is valid
            if not is_valid_network(graph, tree):
                print(solver_filename, 'is invalid!')
                break
            print(solver_filename, 'Nodes: ', tree.nodes)
            for e in tree.edges:
                print("edge:", e, "; weight:", weight(tree, e))
            print(solver_filename, 'Average cost: ', average_pairwise_distance(tree))

            out_file = os.path.join(OUTPUT_DIRECTORY, input_filename[:-3], solver_filename + '.out')
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            write_output_file(tree, out_file)

            print(solver_filename, 'completed in average time:', sum(times) / len(times))
            print()
