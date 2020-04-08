import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys

from queue import PriorityQueue
import numpy as np

# Global variables
G = None
n = 0
required = []
all_visited = []
optional = []
T = None


# Initializes global variables to correct sizes
def instantiate_arrays():
    global required
    global optional
    global all_visited
    required = n * [False]
    optional = n * [False]
    all_visited = n * [False]


# Adds vertex v to T and assigns neighbors to optional visiting
def visit(v, edge=None, optionals=True):
    all_visited[v] = True
    required[v] = True
    T.add_node(v)
    if edge:
        T.add_edge(edge[0], edge[1], weight=weight(edge))
    if optionals:
        for u in list(G.neighbors(v)):
            optional[u] = True


# Helper for finding all leaf paths -- Traverses each leaf path to trim off non-cycle elements
def traverse_path(v, add_v, visited, prevV):
    if (visited[v]):
        return
    visited[v] = True
    all_visited[v] = True
    if (add_v):
        if (prevV != -1):
            visit(v, (v, prevV), False)
        else:
            visit(v, None, False)
        if len(list(G.neighbors(v))) > 2:
            for u in list(G.neighbors(v)):
                optional[u] = True
            return
        else:
            for adj in list(G.neighbors(v)):
                traverse_path(adj, True, visited, v)
    else:
        traverse_path(list(G.neighbors(v))[0], True, visited, -1)


# Finds all leaf paths in G and sets all vertices in path to visited
def find_all_leaf_paths(G):
    leaves = [v for v in G.nodes if len(list(G.neighbors(v))) == 1]
    for leaf in leaves:
        visited = len(list(G.nodes)) * [False]
        traverse_path(leaf, False, visited, None)


# Gets the weight of specified edge
def weight(e):
    edge_dict = G.get_edge_data(e[0], e[1])
    return edge_dict["weight"]


# Finds the minimum edge in edges list or returns 0 if no elements in edges
def minEdge(edges):
    if edges:
        return min(edges)
    return 0


# Finds the minimum edge weight of all of u's outoing edges except for the edge (u,v)
def minEdgeWeight(u, v):
    return minEdge([weight(e) for e in list(G.edges(u)) if e[0] != v and e[1] != v])


# Calculates the initial heuristic if there are no leaf/required elements for first step
def maxHeuristic(G):
    maxH = 0
    maxV = -1
    for v in list(G.nodes):
        minVEdge = minEdge([weight(e) for e in list(G.edges(v))])
        # h = sum([minEdge([weight(e, G) for e in list(G.edges(u)) if e[0] != v and e[1] != v]) for u in list(G.neighbors(v))]) / minVEdge
        h = sum([minEdgeWeight(u, v) * len(list(G.edges(u))) for u in list(G.neighbors(v))]) / minVEdge
        # h = sum([minEdge([weight(e, G) for e in list(G.edges(u))]) for u in list(G.neighbors(v))])
        print("v:", v, "h:", h)
        if (h >= maxH):
            maxH = h
            maxV = v
    return maxV


# Heuristic helper to approximate number of nodes left to visit
def nodes_left():
    return n - np.count_nonzero([sum(x) for x in zip(optional, all_visited)]) + 1


# Calculates heuristic of u based on all non-visited, non-optional neighbors
def calculate_heuristic(u, v):
    sum = 0
    for x in list(G.neighbors(u)):
        if required[x] or optional[x]:
            continue
        sum += minEdgeWeight(x, u) * len(list(G.edges(x)))
    print(u, " to ", v, "h:", sum / (weight((u, v)) ** 2 * nodes_left()))
    return sum / (weight((u, v)) ** 2 * nodes_left())


# Solve helper to greedily find next optimal edge according to heuristic and add it
def solve_graph(G, q):
    while q:
        e = q.get()[1]
        v = e[0]
        if (np.count_nonzero([sum(x) for x in zip(optional, all_visited)]) == n):
            return
        if all_visited[v]:
            continue
        visit(v, e)
        print("Calculating heuristics after visiting", v)
        for u in list(G.neighbors(v)):
            if not all_visited[u]:
                q.put((-calculate_heuristic(u, v), (u,v)))


# Initializes the pq with beginning elements
def initialize_pq(q):
    for i in range(len(required)):
        if (required[i]):
            for u in list(G.neighbors(i)):
                if not all_visited[u]:
                    q.put((-calculate_heuristic(u, i), (u,i)))


# Original solve method
def solve(inputGraph):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    global G
    global n
    global T
    G = inputGraph
    n = len(list(G.nodes))
    T = nx.Graph()

    instantiate_arrays()
    find_all_leaf_paths(G)
    if not any(required):
        chosenV = maxHeuristic(G)
        visit(chosenV)
    q = PriorityQueue()
    initialize_pq(q)
    solve_graph(G, q)
    print(required)
    print(T.edges)
    return T




def test():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8])
    G.add_edge(0, 1, weight=1)
    G.add_edge(1, 2, weight=2)
    G.add_edge(0, 2, weight=1)
    G.add_edge(0, 3, weight=3)
    G.add_edge(3, 4, weight=5)
    G.add_edge(4, 5, weight=2)
    G.add_edge(3, 5, weight=4)
    G.add_edge(0, 6, weight=3)
    G.add_edge(0, 7, weight=2)
    G.add_edge(7, 8, weight=3)
    solve(G)


def test2():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edge(0, 1, weight=2)
    G.add_edge(0, 2, weight=2)
    G.add_edge(0, 3, weight=2)
    G.add_edge(0, 4, weight=2)
    G.add_edge(0, 5, weight=2)
    G.add_edge(0, 6, weight=2)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    G.add_edge(6, 7, weight=1)
    solve(G)


def test3():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
    G.add_edge(0, 1, weight=2)
    G.add_edge(0, 2, weight=2)
    G.add_edge(0, 3, weight=2)
    G.add_edge(0, 4, weight=2)
    G.add_edge(0, 5, weight=2)
    G.add_edge(0, 6, weight=2)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    solve(G)


def test4():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4])
    G.add_edge(0, 1, weight=1)
    G.add_edge(0, 2, weight=3)
    G.add_edge(1, 3, weight=2)
    G.add_edge(2, 3, weight=1)
    G.add_edge(1, 4, weight=3)
    G.add_edge(2, 4, weight=2)
    G.add_edge(3, 4, weight=5)
    solve(G)


test()
print()
test2()
print()
test3()
print()
test4()


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
