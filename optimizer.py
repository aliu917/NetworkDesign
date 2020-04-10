"""
Takes a graph and corresponding valid tree and optimizes cost by making three types of adjustments: adding an edge
(and a vertex, removing an (optional) edge (and vertex, or replacing an edge (while keeping same vertices). Runs
until no immediate changes lead to improvements.
"""
import random

from networkx import Graph, find_cycle

from utils import average_pairwise_distance


def optimize(graph: Graph, tree: Graph, orig_cost: float):
    # get all edges to consider
    edges = []
    for node in tree.nodes:
        for neighbor in graph.neighbors(node):
            if neighbor not in tree.nodes:
                edges.append((node, neighbor))

    # for each edge (consider order randomly)
    while edges:
        added_edge = random.choice(edges)
        add_edge(tree, added_edge)

        # if added edge creates a cycle
        if added_edge[1] in tree.nodes:
            cycle: list = find_cycle(tree, added_edge[0])
            try:
                cycle.remove(added_edge)
            except ValueError:
                cycle.remove(added_edge[::-1])

            replaced_edge, new_cost = optimize_removal(tree, cycle, orig_cost)

            if replaced_edge:
                remove_edge(tree, replaced_edge)
                return optimize(graph, tree, new_cost)
            else:
                remove_edge(tree, added_edge)
        # if other vertex not in tree
        else:
            tree.add_node(added_edge[1])
            add_edge(tree, added_edge)

            new_cost = average_pairwise_distance(tree)

            if new_cost < orig_cost:
                return optimize(graph, tree, new_cost)
            else:
                remove_edge(tree, added_edge)
                tree.remove_node(added_edge[1])

        # remove considered edge
        edges.remove(added_edge)


def optimize_removal(tree: Graph, cycle: list, orig_cost: float):
    """
    Returns the first edge found in the cycle which, if removed from tree, leads to a decrease in cost (average pairwise
    distance).
    :param tree: tree (with 1 extra edge) to consider
    :param cycle: list of edges to consider (which form a cycle, removal of any restores tree)
    :param orig_cost: original cost
    :return:
    """
    for edge in cycle:
        remove_edge(tree, edge)
        new_cost = average_pairwise_distance(tree)
        add_edge(tree, edge)
        if new_cost < orig_cost:
            return edge, new_cost

    return None, orig_cost


# Helper Functions
def remove_edge(graph: Graph, edge: tuple):
    graph.remove_edge(edge[0], edge[1])


def add_edge(graph: Graph, edge: tuple):
    graph.add_edge(edge[0], edge[1], weight=graph[edge[0]][edge[1]]['weight'])
