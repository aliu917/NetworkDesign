from networkx import Graph
import networkx as nx
from networkx.algorithms import approximation as ap
from utils import is_valid_network


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    H = G.copy()
    for v in list(G.nodes):
        if len(list(G.neighbors(v))) == len(G.nodes) - 1:
            t = nx.Graph()
            t.add_node(v)
            return t
    t = find_dom_tree(G)
    check = is_valid_network(H, t)
    if not check:
        raise Exception('invalid')
    return t


def find_dom_tree(graph: Graph):
    """
    Finds an approximate small dominating tree.
    :param graph: Graph on which to find the tree
    :return: tree
    """
    augmented = augment(graph)
    dom_set = ap.min_weighted_dominating_set(augmented, 'weight')
    restore(dom_set)
    new_graph = de_augment(dom_set, graph)
    return shortest_paths(new_graph)


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
    return graph[u][v]['weight']  # TODO: implement


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


def mst(graph: Graph):
    """
    Uses an mst algorithm to find a tree from a graph
    :param graph: graph to consider
    :return: tree
    """
    return nx.minimum_spanning_tree(graph)


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
                edges.add((prev, node))
            prev = node
    new = Graph()
    if edges:
        new.add_edges_from(edges)
    else:
        new.add_node(center)
    return new


def most_between(graph: Graph):
    """
    Returns the tree by selecting edges of increasing betweeness centrality which do not create cycles.
    :param graph: graph on which to build tree
    :return: tree with betweeness nodes
    """
    # TODO: implement
    pass

# g = nx.cycle_graph(5)
# aug = augment(g)
# nx.draw(g)
# nx.draw(aug)
