import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys

from queue import PriorityQueue
import numpy as np
from disjoint_set import DisjointSet
from graph import Graph
from simple_tests import run_all_tests


# Original solve method
def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    g = Graph(G)
    T = g.dijkstra_solve_graph()
    return T

# run_all_tests(solve)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')
