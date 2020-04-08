"""
Runs all solvers in solvers.txt on all graphs in specified directory (inputs\25),
writing the outputs to corresponding entries in specified directory (outputs\25).

Usage: python runner.py inputs\25 outputs\25
"""

from parse import read_input_file, write_output_file
from utils import is_valid_network

import sys
from importlib import import_module
from os import listdir
from time import time

if __name__ == '__main__':
    assert len(sys.argv) == 3
    SOLVERS_FILENAME = 'solvers.txt'
    INPUT_DIRECTORY = sys.argv[1]
    OUTPUT_DIRECTORY = sys.argv[2]

    MAX_SIZE = 100

    with open(SOLVERS_FILENAME) as f:
        solvers = f.read().splitlines()

    input_filenames = listdir(INPUT_DIRECTORY)

    # for each solver
    for solver_filename in solvers:

        # get the solver from module name
        mod = import_module(solver_filename)
        solve = getattr(mod, 'solve')

        times = []
        # for each graph
        for input_filename in input_filenames:
            input_path = INPUT_DIRECTORY + '\\' + input_filename
            graph = read_input_file(input_path, MAX_SIZE)
            start = time()
            tree = solve(graph)
            end = time()
            times.append(end - start)
            # check if the output is valid
            if not is_valid_network(graph, tree):
                print(solver_filename, 'is invalid!')
                break

            output_path = OUTPUT_DIRECTORY + '\\' + input_filename + '\\' + solver_filename
            with open(input_path, 'w') as f:
                write_output_file(tree, f)

        print(solver_filename, 'completed in average time:', sum(times) / len(times))
