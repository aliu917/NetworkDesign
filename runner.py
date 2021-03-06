"""
Runs all solvers in solvers.txt on all graphs in specified directory (our_inputs\25),
writing the our_outputs to corresponding entries in specified directory (our_outputs\25).

Usage: python runner.py our_inputs\25 our_outputs\25
"""
import csv
import os
import sys
from importlib import import_module
from os import listdir
from os.path import join
from time import time
import networkx as nx

from graphsolver import weight
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance

saved_costs = [0] * 8


def main():
    global saved_costs
    assert len(sys.argv) == 3
    SOLVERS_FILENAME = 'solvers.txt'
    INPUT_DIRECTORY = sys.argv[1]
    OUTPUT_DIRECTORY = sys.argv[2]
    RESULTS_FILENAME = join('our_outputs', 'results.csv')

    MAX_SIZE = 100
    overall_start = time()

    with open(SOLVERS_FILENAME, 'r') as f:
        solvers = f.read().splitlines()

    input_filenames = os.listdir(INPUT_DIRECTORY)

    all_costs = []
    all_times = []
    for _ in solvers:
        all_costs.append([])
        all_times.append([])

    # for each graph
    input_filenames.sort()
    # for input_filename in ["small-150.in"]:

    for input_filename in input_filenames:
        costs_iter = iter(all_costs)
        times_iter = iter(all_times)
        print("File name:", input_filename)
        # for each solver
        for solver_filename in solvers:
            costs = next(costs_iter)
            times = next(times_iter)
            # get the solver from module name
            mod = import_module(solver_filename)
            solve = getattr(mod, 'solve')

            if input_filename == 'small-206.in':
                print('stop!')  # breakpoint for debugging

            input_path = os.path.join(INPUT_DIRECTORY, input_filename)
            graph = read_input_file(input_path, MAX_SIZE)
            start = time()
            tree = solve(graph)
            end = time()
            times.append(end - start)

            if not is_valid_network(graph, tree):
                print(solver_filename, 'is invalid!')
                nx.draw(graph)
                return

            # print(solver_filename, 'Nodes: ', tree.nodes)
            # for e in tree.edges:
            #     print("edge:", e, "; weight:", weight(graph, e))
            cost = average_pairwise_distance(tree)
            print(solver_filename, 'Average cost: ', cost)
            costs.append(cost)

            out_file = os.path.join(OUTPUT_DIRECTORY, input_filename[:-3], solver_filename + '.out')
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            write_output_file(tree, out_file)

            print(solver_filename, 'completed in average time:', sum(times) / len(times))
        print()

    name_iter = iter(solvers)
    for avg_costs in all_costs:
        name = next(name_iter)
        if len(avg_costs) == 0:
            print("Errored somewhere")
            break
        average = sum(avg_costs) / len(avg_costs)
        avg_costs.append(average)
        print(name, 'average cost:', average)
    # print()
    name_iter = iter(solvers)
    for times in all_times:
        name = next(name_iter)
        average = sum(times) / len(times)
        print(name, 'average time', average)
    print("Saved costs:", saved_costs)

    # add headers
    graph_names = input_filenames
    graph_names.append('Average')
    all_costs.insert(0, graph_names)

    with open(RESULTS_FILENAME, 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerows(all_costs)

    overall_end = time()
    print("Overall time: ", overall_end - overall_start)


if __name__ == '__main__':
    main()
