from graphsolver import GraphSolver
from graphsolver import weight, process, centrality
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
from simple_tests import test6


# Calculates the initial heuristic if there are no leaf/required elements for first step
def heuristic(G, e):
    cost = weight(G, e)
    v1 = e[0]
    v2 = e[1]
    central = centrality(v1) * centrality(v2)
    return cost ** 2 / central

def first_heuristic(g):
    maxH = 0
    maxV = -1
    for v in list(g.G.nodes):
        if len(list(g.neighbors(v))) == g.n - 1:  # Special case when one vertex is connected to all of them
            return v
        minVEdge = g.minEdge([weight(g.G, e) for e in list(g.edges(v))])
        # h = sum([minEdge([weight(e, G) for e in list(G.edges(u)) if e[0] != v and e[1] != v]) for u in list(G.neighbors(v))]) / minVEdge
        h = sum([g.minEdgeWeight(u, v) * len(list(g.edges(u))) for u in list(g.neighbors(v))]) / minVEdge
        # h = sum([minEdge([weight(e, G) for e in list(G.edges(u))]) for u in list(G.neighbors(v))])
        # print("v:", v, "h:", h)
        if (h >= maxH):
            maxH = h
            maxV = v
    return maxV

# Original solve method
def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    g = GraphSolver(G)
    single_node = process(g)
    if single_node >= 0:
        return g.T
    g.visit(first_heuristic(g))
    T = g.mst_solve_graph(heuristic)
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
