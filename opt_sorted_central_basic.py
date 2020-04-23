from graphsolver import GraphSolver
from graphsolver import weight
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
from simple_tests import test6

# Good for small-150, small-160, small-168, small-17, small-174, small-176
isDeterministic = False

# Calculates the initial heuristic if there are no leaf/required elements for first step
def first_heuristic(g):
    maxH = 0
    maxV = -1
    for v in list(g.G.nodes):
        if len(list(g.neighbors(v))) == g.n - 1:  # Special case when one vertex is connected to all of them
            return v
        h = g.node_centrality(v)
        if (h >= maxH):
            maxH = h
            maxV = v

    return maxV


# Calculates heuristic of u based on all non-visited, non-optional neighbors
def calculate_heuristic(g, u, v):
    # print(u, " to ", v, "h:", sum / (g.weight((u, v)) * g.nodes_left()))
    return weight(g.G, (u, v))


# Original solve method
def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    g = GraphSolver(G)
    T = g.dijkstra_solve_graph(None, calculate_heuristic, first_heuristic)
    if average_pairwise_distance(T) == 0:
        return T
    optimize_sorted(g, T, cycle_killer_fn=kill_cycle)
    return T

# test6(solve)


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
