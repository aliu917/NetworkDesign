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

    graphs = [read_input_file(path, MAX_SIZE) for path in listdir(INPUT_DIRECTORY)]

    # for each solver
    for filename in solvers:
        path = OUTPUT_DIRECTORY + '\\' + filename
        # get the solver from module name
        mod = import_module(filename)
        solve = getattr(mod, 'solve')

        times = []
        # for each graph
        for graph in graphs:
            start = time()
            tree = solve(graph)
            end = time()
            times.append(end - start)
            # check if the output is valid
            if not is_valid_network(graph, tree):
                print(filename, 'is invalid!')
                break

            with open(path, 'w') as f:
                write_output_file(tree, path)

        print(filename, 'completed in average time:', sum(times) / len(times))
