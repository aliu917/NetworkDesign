from networkx import Graph
import networkx as nx
from networkx.algorithms import approximation as ap
from utils import is_valid_network
from queue import PriorityQueue
from networkx.algorithms.centrality import edge_betweenness_centrality

from graphsolver import GraphSolver
from optimizer_sorted import optimize_sorted, kill_cycle_all_paths


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    t = most_between(G)
    solver = GraphSolver(G)
    for node in t.nodes:
        solver.visit(node)
    for edge in t.edges:
        solver.add_edge(edge)
    optimize_sorted(solver, solver.T, kill_cycle_all_paths)
    return solver.T


def most_between(graph: Graph):
    """
    Returns the tree by selecting edges of increasing betweeness centrality which do not create cycles (Kruskal).
    :param graph: graph on which to build tree
    :return: tree with betweeness nodes
    """

    # def add_neighbors(U):
    #     """
    #     Adds all neighbors of node in graph to q.
    #     :param U: node whose neighbors we add
    #     """
    #     for V in graph[U]:
    #         if (U, V) in betweenness:
    #             if not nx.has_path(new, U, V):
    #                 q.put((-betweenness[U, V], U, V))
    #             continue
    #         if (V, U) in betweenness:
    #             if not nx.has_path(new, U, V):
    #                 q.put((-betweenness[V, U], U, V))
    #             continue

    new = Graph()
    new.add_nodes_from(graph.nodes)

    betweenness = edge_betweenness_centrality(graph)
    q = PriorityQueue()
    for u, v in graph.edges:
        if (u, v) in betweenness:
            q.put((-betweenness[u, v], u, v))
            continue
        if (v, u) in betweenness:
            q.put((-betweenness[v, u], v, u))
            continue

    # for u in nodes:
    #     add_neighbors(u)

    while not nx.is_connected(new):
        bet, u, v = q.get()
        if not nx.has_path(new, u, v):
            new.add_edge(u, v, weight=graph[u][v]['weight'])
            # add_neighbors(u)

    return new

# g = nx.cycle_graph(5)
# aug = augment(g)
# nx.draw(g)
# nx.draw(aug)
