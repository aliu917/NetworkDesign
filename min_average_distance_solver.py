from graphsolver import GraphSolver
from graphsolver import weight
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
from networkx import closeness_centrality
from simple_tests import test6

isDeterministic = False

# Calculates the initial heuristic if there are no leaf/required elements for first step
def first_heuristic(g):
    maxH = 0
    maxV = -1
    for v in list(g.G.nodes):
        if len(list(g.neighbors(v))) == g.n - 1:  # Special case when one vertex is connected to all of them
            return v

        ave_edge = sum([weight(g.G, e) for e in list(g.edges(v))]) / g.G.degree[v]
        h = g.node_centrality(v) / ave_edge
    #     # h = sum([minEdge([weight(e, G) for e in list(G.edges(u)) if e[0] != v and e[1] != v]) for u in list(G.neighbors(v))]) / minVEdge
    #     h = sum([g.minEdgeWeight(u, v) * len(list(g.edges(u))) for u in list(g.neighbors(v))]) / minVEdge
    #     # h = sum([minEdge([weight(e, G) for e in list(G.edges(u))]) for u in list(G.neighbors(v))])
    #     # print("v:", v, "h:", h)
        if (h >= maxH):
            maxH = h
            maxV = v

    return maxV


# Calculates heuristic of u based on all non-visited, non-optional neighbors
def calculate_heuristic(g, u, v):
    g.visit(u)
    x_centrality = closeness_centrality(g.T, u, "weight")
    g.unvisit(u)
    return x_centrality


# Original solve method
def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    g = GraphSolver(G)
    start = g.find_leaf_path()
    T = g.dijkstra_solve_graph(start, calculate_heuristic, first_heuristic)
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
