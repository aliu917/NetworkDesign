"""
Runs all solvers in solvers.txt on all graphs in specified directory (inputs\25),
writing the outputs to corresponding entries in specified directory (outputs\25).

Usage: python runner.py inputs\25 outputs\25
"""
import csv
import os
import sys
import json
from importlib import import_module
from os import listdir
from os.path import join
from time import time
import networkx as nx

from graphsolver import weight
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance


def main():
    assert len(sys.argv) == 3
    SOLVERS_FILENAME = 'solvers.txt'
    INPUT_DIRECTORY = sys.argv[1]
    OUTPUT_DIRECTORY = sys.argv[2]
    RESULTS_FILENAME = join('outputs', 'results.csv')
    PREV_OUTPUTS_FILENAME = join(OUTPUT_DIRECTORY, 'all_prev_outputs.txt')

    MAX_SIZE = 100

    with open(SOLVERS_FILENAME, 'r') as f:
        solvers = f.read().splitlines()

    input_filenames = os.listdir(INPUT_DIRECTORY)

    all_costs = [] # dimension 1 = solver i, dimension 2 = cost for input j
    all_times = []
    for _ in solvers:
        all_costs.append([])
        all_times.append([])

    print('um', PREV_OUTPUTS_FILENAME)
    if os.path.isfile(PREV_OUTPUTS_FILENAME):
        with open(PREV_OUTPUTS_FILENAME, 'r') as f:
            all_prev_outputs = json.load(f)
    else:
        # Key: input filename
        # Value: {best: solver_filename, data: {solver_filename: {cost: x, time: x}}
        all_prev_outputs = {}

    # for each graph
    input_filenames.sort()
    # for input_filename in ["small-150.in"]:
    for input_filename in input_filenames:
        costs_iter = iter(all_costs)
        times_iter = iter(all_times)
        # print('costs_iter', costs_iter.peek())
        print("File name:", input_filename)

        # {best: solver_filename, data: {solver_filename: {cost: x, runtime: x}}
        prev_outputs = all_prev_outputs.get(input_filename, {'best': None, 'data': {}})
        if prev_outputs['best'] is None:
            # Hasn't been run before
            all_prev_outputs[input_filename] = prev_outputs

        # for each solver
        for solver_filename in solvers:
            costs = next(costs_iter)
            times = next(times_iter)
            # get the solver from module name
            mod = import_module(solver_filename)
            solve = getattr(mod, 'solve')
            mod.input_filename = input_filename # pass this to the combined solver
            mod.OUTPUT_DIRECTORY = OUTPUT_DIRECTORY

            if getattr(mod, 'isDeterministic', False) and solver_filename in prev_outputs['data'].keys():
                print('{} skipped computation because it is deterministic and was run before'.format(solver_filename))

                cost = prev_outputs['data'][solver_filename]['cost']
                runtime = prev_outputs['data'][solver_filename]['runtime']

                times.append(runtime)
                print(solver_filename, 'Average cost: ', cost)
                costs.append(cost)
                print(solver_filename, 'completed in average time:', sum(times) / len(times))
                continue

            # if input_filename == 'small-206.in':
            #     print('stop!')  # breakpoint for debugging

            input_path = os.path.join(INPUT_DIRECTORY, input_filename)
            graph = read_input_file(input_path, MAX_SIZE) # probably inefficient to do this all the time
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
            print(solver_filename, 'completed in average time:', sum(times) / len(times))

            # Update prev_outputs and .out only if a previous run was worse or it was never saved before
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

    # add headers
    graph_names = input_filenames
    graph_names.append('Average')
    all_costs.insert(0, graph_names)

    with open(RESULTS_FILENAME, 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerows(all_costs)

    with open(PREV_OUTPUTS_FILENAME, 'w') as f:
        json.dump(all_prev_outputs, f, indent=2)

if __name__ == '__main__':
    main()
