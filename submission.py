import csv
import os
import sys
from importlib import import_module
from os import listdir
from os.path import join
from time import time
import networkx as nx

from graphsolver import weight
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_network, average_pairwise_distance
from shutil import copyfile

def main():
    SOLVERS_FILENAME = 'solvers.txt'
    INPUT_DIRECTORY = ["inputs/large", "inputs/medium", "inputs/small"]
    OUTPUT_DIRECTORY = ["outputs/large", "outputs/medium", "outputs/small"]
    SUBMISSION_DIRECTORY = "outputs/submission"

    with open(SOLVERS_FILENAME, 'r') as f:
        solvers = f.read().splitlines()

    solver = "dummy"
    while solver not in solvers:
        solver = input("Please input a solver name.")

    input_filenames = {}
    for d in INPUT_DIRECTORY:
        f_lst = os.listdir(d)
        f_lst.sort()
        input_filenames[d] = f_lst

    all_costs = []

    for sizes in OUTPUT_DIRECTORY:
        graphs = os.listdir(sizes)
        graphs.sort()
        for graph in graphs:
            if "txt" in graph:
                continue
            for f in os.listdir(os.path.join(sizes, graph)):
                if solver not in f:
                    continue
                out_file = os.path.join(SUBMISSION_DIRECTORY, graph + '.out')
                os.makedirs(os.path.dirname(out_file), exist_ok=True)
                copyfile(os.path.join(sizes, graph, f), out_file)
                input_path = os.path.join("inputs", os.path.basename(sizes), graph) + ".in"
                g = read_input_file(input_path, 100)
                tree = read_output_file(out_file, g)
                cost = average_pairwise_distance(tree)
                all_costs.append(cost)
                print(graph, ":", cost)
    average = sum(all_costs) / len(all_costs)
    print()
    print('Overall average cost:', average)

if __name__ == '__main__':
    main()