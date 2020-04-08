"""
Computes the costs of all graphs in the specified directory (outputs\25), writing the results to a csv file

Usage: python tester.py outputs/25 [results.csv]
"""
import csv
import sys
from os import listdir
from os.path import isdir, join

from parse import read_output_file_unsafe
from utils import average_pairwise_distance

if __name__ == '__main__':
    assert len(sys.argv) <= 3
    OUTPUTS_DIRECTORY = sys.argv[1]
    RESULTS_FILENAME = 'results.csv'
    if len(sys.argv) == 3:
        RESULTS_FILENAME = sys.argv[2]

    # initialize array holding all_costs
    directories = [f for f in listdir(OUTPUTS_DIRECTORY) if isdir(join(OUTPUTS_DIRECTORY, f))]
    tem_dir = listdir(OUTPUTS_DIRECTORY + '\\' + directories[0])
    all_costs = []
    for _ in tem_dir:
        all_costs.append([])

    # for each directory/graph
    for directory in directories:
        outs = listdir(OUTPUTS_DIRECTORY + '\\' + directory)
        # for each solver (on this graphg)
        for i in range(len(outs)):
            tree = read_output_file_unsafe(OUTPUTS_DIRECTORY + '\\' + directory + '\\' + outs[i])
            all_costs[i].append(average_pairwise_distance(tree))

    # add averages
    for avg_costs in all_costs:
        avg_costs.append(sum(avg_costs) / len(avg_costs))

    # add headers
    graph_names = directories
    graph_names.append('Average')
    all_costs.insert(0, graph_names)

    with open(RESULTS_FILENAME, 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerows(all_costs)
