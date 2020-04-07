"""
Tests all solvers specified in SOVLERS_FILENAME (default: solvers.txt) on all
graphs in the specified directory, outputting the costs for each solver on
each graph and the average into a csv file (default: results.csv).

TODO: implement new version in which a seperate script generates all .out...
graphs and this script simply reads the .out graphs and computes cost
"""
from importlib import import_module
from utils import is_valid_network, average_pairwise_distance
import csv

SOLVERS_FILENAME = 'solvers.txt'
GRAPHS_DIRECTORY = 'test'  # TODO: update directory name
RESULTS_FILENAME = 'results.csv'

# TODO: Read all graphs in GRAPHS_DIRECTORY and assign to list graphs
graphs = []
# TODO: Read graph names and write to list graph_names
graph_names = []

# contains lists for each solver which records the average distance
all_costs = []

with open(SOLVERS_FILENAME) as f:
    solvers = f.read().splitlines()

# for each solver
for filename in solvers:
    avg_costs = []
    # get the solver from module name
    mod = import_module(filename)
    solve = getattr(mod, 'solve')
    # for each graph
    for graph in graphs:
        tree = solve(graph)  # TODO: analyze runtime?
        # check if the output is valid
        if not is_valid_network(graph, tree):
            print(filename, 'is invalid!')
            break
        avg_costs.append(average_pairwise_distance(tree))

num_graphs = len(graphs)
for avg_costs in all_costs:
    avg_costs.append(sum(avg_costs) / num_graphs)

graph_names.append('Average')
all_costs.insert(0, graph_names)

with open(RESULTS_FILENAME, 'w', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(all_costs)
