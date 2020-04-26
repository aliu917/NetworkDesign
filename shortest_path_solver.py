from networkx import Graph
import networkx as nx
from networkx.algorithms import approximation as ap
from queue import PriorityQueue
from networkx.algorithms.centrality import edge_betweenness_centrality

from graphsolver import GraphSolver
from optimizer_sorted import optimize_sorted, kill_cycle_all_paths
from utils import is_valid_network

isDeterministic = False

def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    t = find_shortest_paths(G)
    solver = GraphSolver(G)
    for node in t.nodes:
        solver.visit(node)
    for edge in t.edges:
        solver.add_edge(edge)
    optimize_sorted(solver, solver.T, kill_cycle_all_paths)

    check = is_valid_network(G, solver.T)
    if not check:
        raise Exception('invalid')
    return solver.T


def find_shortest_paths(graph: Graph):
    """
    Finds an approximate small dominating tree.
    :param graph: Graph on which to find the tree
    :return: tree
    """
    # augmented = augment(graph)
    # dom_set = ap.min_weighted_dominating_set(augmented, 'weight')
    # restore(dom_set)
    # new_graph = de_augment(dom_set, graph)
    # return shortest_paths(new_graph)
    return shortest_paths(graph)


# Functions to augment the tree
# noinspection PyUnresolvedReferences
def augment(base: Graph):
    """
    Creates an augmented version of G with added vertices along each edge. Assumes str of node names are unique.
    :param base: graph on which to augment
    :return: new graph
    """
    new = Graph()
    # add original nodes
    for node in base.nodes:
        new.add_node(node, weight=base_weight(node, base))
    # add new nodes
    for edge in base.edges:
        name = edge
        w = augmented_weight(edge, base)
        new.add_node(name, weight=w)
        # add edges
        for end in edge:
            if base.degree[end] > 1:
                new.add_edge(name, end)
    return new


# noinspection PyUnresolvedReferences
def base_weight(node, graph: Graph):
    """
    Computes and returns the weight of a node.
    :param node: node to be considered
    :param graph: parent graph
    :return: node weight
    """
    if graph.degree[node]:
        return sum([graph[node][neighbor]['weight'] for neighbor in graph.neighbors(node)]) / graph.degree[node]
    else:  # to avoid divide by zero (no neighbors) error, occurs with singleton graphs
        return 1
    # TODO: implement


def augmented_weight(edge, graph: Graph):
    """
    Computes and returns the weight of a node augmented along a pre-existing edge.
    :param edge: edge on which to augment node
    :param graph: parent graph
    :return: weight
    """
    u, v = edge
    return graph[u][v]['weight'] * 2 ** 10  # TODO: implement


# Functions to convert the selected nodes

def restore(nodes: set):
    """
    Converts the set of node names selected in then augmented graph to a corresponding set in the base graph.
    :param nodes: nodes selected in the augmented graph
    """
    for node in nodes.copy():
        if type(node) == tuple:
            nodes.add(int(node[0]))
            nodes.add(int(node[1]))
            nodes.remove(node)


def de_augment(nodes: set, graph: Graph):
    """
    Takes the nodes selected from an augmented graph and builds a corresponding graph with original edges and nodes.
    :param nodes: selected nodes from augmented graph
    :param graph: base graph
    :return: graph with original edges and selected nodes
    """
    new = Graph()
    # add all nodes and all possible edges
    new.add_nodes_from(nodes)
    for node1 in nodes:
        for node2 in nodes:
            if graph.has_edge(node1, node2):
                new.add_edge(node1, node2, weight=graph[node1][node2]['weight'])

    return new


# def mst(graph: Graph):
#     """
#     Uses an mst algorithm to find a tree from a graph
#     :param graph: graph to consider
#     :return: tree
#     """
#     return nx.minimum_spanning_tree(graph)


def shortest_paths(graph: Graph):
    """
    Returns the shortest paths tree from the node with the highest betweenness centrality among trees.
    :param graph: graph to consider
    :return: shortest path tree
    """

    betweenness = nx.betweenness_centrality(graph)
    center = max(betweenness, key=betweenness.get)
    distances, paths = nx.algorithms.shortest_paths.single_source_dijkstra(graph, center)

    edges = set()
    for path in paths.values():
        prev = None
        for node in path:
            if prev is not None:
                edges.add((prev, node, graph[prev][node]['weight']))
            prev = node
    new = Graph()
    if edges:
        for edge in edges:
            new.add_edge(edge[0], edge[1], weight=edge[2])
    else:
        new.add_node(center)
    return new
