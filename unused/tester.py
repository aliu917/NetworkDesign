"""
Computes the costs of all graphs in the specified directory (outputs\25), writing the results to a csv file.

Currently doesn't calculate accurately, fix if running runner takes too much time.

Usage: python tester.py outputs/25 [outputs/results.csv]
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
    RESULTS_FILENAME = join('outputs', 'results.csv')
    if len(sys.argv) == 3:
        RESULTS_FILENAME = sys.argv[2]

    # initialize array holding all_costs
    directories = [f for f in listdir(OUTPUTS_DIRECTORY) if isdir(join(OUTPUTS_DIRECTORY, f))]
    if not directories:
        print('no directories/graphs!')
        sys.exit(1)

    tem_dir = listdir(join(OUTPUTS_DIRECTORY, directories[0]))
    all_costs = []
    for _ in tem_dir:
        all_costs.append([])

    # for each directory/graph
    for directory in directories:
        outs_dir = join(OUTPUTS_DIRECTORY, directory)
        outs = listdir(outs_dir)
        # for each solver (on this graph)
        for i in range(len(outs)):
            tree = read_output_file_unsafe(join(outs_dir, outs[i]))
            all_costs[i].append(average_pairwise_distance(tree))

    # noinspection PyUnboundLocalVariable
    name_iter = iter(outs)
    for avg_costs in all_costs:
        average = sum(avg_costs) / len(avg_costs)
        avg_costs.append(average)
        print(next(name_iter), 'average cost:', average)

    # add headers
    graph_names = directories
    graph_names.append('Average')
    all_costs.insert(0, graph_names)

    with open(RESULTS_FILENAME, 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerows(all_costs)
