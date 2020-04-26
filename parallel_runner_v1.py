"""
Runs all solvers in solvers.txt on all graphs in specified directory (inputs\25),
writing the outputs to corresponding entries in specified directory (outputs\25).

Usage: python runner.py inputs\25 outputs\25
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
import multiprocessing
from multiprocessing import Pool
import multiprocessing.pool

from utils import Cacher
from multiprocessing import Manager
from multiprocessing.managers import BaseManager


saved_costs = [0] * 8

INPUT_DIRECTORY = sys.argv[1]
OUTPUT_DIRECTORY = sys.argv[2]
RESULTS_FILENAME = join('outputs', 'results.csv')

MAX_SIZE = 100

all_costs = []
all_times = []
SOLVERS_FILENAME = 'solvers.txt'
with open(SOLVERS_FILENAME, 'r') as f:
    solvers = f.read().splitlines()
for _ in solvers:
    all_costs.append([])
    all_times.append([])

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def solve_graph(config):
    input_filenames, cacher = config
    for input_filename in input_filenames:
        global all_costs
        global all_times
        costs_iter = iter(all_costs)
        times_iter = iter(all_times)
        # print("File name:", input_filename)
        # for each solver
        for solver_filename in solvers:
            costs = []
            times = []
            # get the solver from module name
            mod = import_module(solver_filename)
            solve = getattr(mod, 'solve')

            # pass these to the combined solver
            mod.cacher = cacher
            mod.OUTPUT_DIRECTORY = OUTPUT_DIRECTORY
            mod.input_filename = input_filename 

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
            print(solver_filename, 'running', input_filename, '\n Average cost: ', cost, '\n Average time:', sum(times) / len(times), '\n')
            costs.append(cost)

            out_file = os.path.join(OUTPUT_DIRECTORY, input_filename[:-3], solver_filename + '.out')
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            write_output_file(tree, out_file)

        # print('\n\n\n\n\nfinal data', cacher.get_cache(), '\n\n\n\n\n\n')

            # print(solver_filename, 'completed in average time:', sum(times) / len(times))


def main():
    global saved_costs
    assert len(sys.argv) == 3
    overall_start = time()


    input_filenames = os.listdir(INPUT_DIRECTORY)

    # for each graph
    input_filenames.sort()
    # for input_filename in ["small-150.in"]:


    ########### Parallelized ##########################

    BaseManager.register('Cacher', Cacher)
    manager = BaseManager()
    manager.start()

    # Create NUM_THREADS or NUM_THREADS+1 threads
    NUM_THREADS = 4
    INPUTS_PER_SAVE = 10

    NUM_THREADS = min(INPUTS_PER_SAVE, NUM_THREADS)
    for j in range(0, len(input_filenames), INPUTS_PER_SAVE):
        pool = MyPool()

        size = INPUTS_PER_SAVE // NUM_THREADS
        NUM_THREADS += (INPUTS_PER_SAVE > NUM_THREADS*size) # If we need to round up

        cachers = [manager.Cacher(OUTPUT_DIRECTORY) for i in range(NUM_THREADS)]
        pool.map(solve_graph, [(input_filenames[j+i*size:j+(i+1)*size], cachers[i]) \
                                     for i in range(NUM_THREADS)])
        # pool.map(solve_graph, input_filenames)
        pool.close()
        pool.join()

        # Do this in sequence (not parallel) so race conditions don't happen
        data = {}
        for cacher in cachers:
            data = cacher.override(data)

        cachers[0].save_data(data)

    ########### Non - Parallelized ######################

    # solve_graph(input_filename)

    ######################################################

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
    # for times in all_times:
    #     name = next(name_iter)
    #     average = sum(times) / len(times)
    #     print(name, 'average time', average)
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
