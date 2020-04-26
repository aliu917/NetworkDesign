from graphsolver import GraphSolver
from graphsolver import weight
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
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
    sum = 0
    for x in list(g.neighbors(u)):
        if g.is_in_tree(x) or g.is_optional(x):
            continue
        sum += g.minEdgeWeight(x, u) * len(list(g.edges(x)))
    # print(u, " to ", v, "h:", sum / (g.weight((u, v)) * g.nodes_left()))
    return sum / (weight(g.G, (u, v)) * g.nodes_left())


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
    if start is None:
        start = first_heuristic(g)
    graph_choices = []
    for v in g.neighbors(start):
        newG = G.copy()
        new_g = GraphSolver(newG)
        new_g.visit(start)
        new_g.visit(v, (start,v))
        graph_choices.append(new_g)
    minT = G
    minCost = float('inf')
    for g_option in graph_choices:
        g_option.dijkstra_solve_graph(start, calculate_heuristic, first_heuristic)
        optimize_sorted(g_option, g_option.T, cycle_killer_fn=kill_cycle)
        cost = average_pairwise_distance(g_option.T)
        if cost < minCost:
            minCost = cost
            minT = g_option.T
    return minT

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
