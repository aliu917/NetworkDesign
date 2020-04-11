"""
Takes a graph and corresponding valid tree and optimizes cost by making three types of adjustments: adding an edge
(and a vertex, removing an (optional) edge (and vertex, or replacing an edge (while keeping same vertices). Runs
until no immediate changes lead to improvements.
"""
import random

from networkx import Graph, find_cycle

from graphsolver import GraphSolver
from utils import average_pairwise_distance
from graphsolver import edge_exists


def optimize(solver: GraphSolver, tree: Graph, orig_cost: float = None):
    # noinspection PyUnusedLocal
    no_add = no_remove = False

    new_cost = optimize_additions(solver, tree, orig_cost)
    no_add = new_cost == orig_cost
    orig_cost = new_cost

    new_cost = optimize_removal(solver, tree, new_cost)
    no_remove = new_cost == orig_cost

    if no_add and no_remove:
        return

    optimize(solver, tree, new_cost)


def optimize_additions(solver: GraphSolver, tree: Graph, orig_cost: float = None):
    graph = solver.G
    if orig_cost is None:
        orig_cost = average_pairwise_distance(tree)

    # get all edges to consider
    edges = []
    for node in tree.nodes:
        for neighbor in graph.neighbors(node):
            if not edge_exists(tree, (node, neighbor)):
                edges.append((node, neighbor))

    # for each edge (consider order randomly)
    while edges:
        added_edge = random.choice(edges)
        weight = graph[added_edge[0]][added_edge[1]]['weight']

        # if added edge creates a cycle
        if added_edge[1] in tree.nodes:
            solver.add_edge(added_edge)
            cycle: list = find_cycle(tree, added_edge[0])
            try:
                cycle.remove(added_edge)
            except ValueError:
                cycle.remove(added_edge[::-1])

            replaced_edge, new_cost = kill_cycle(solver, cycle, orig_cost)

            if replaced_edge:
                solver.remove_edge(replaced_edge)
                return optimize_additions(solver, tree, new_cost)
            else:
                solver.remove_edge(added_edge)
        # if other vertex not in tree
        else:
            v = added_edge[1]
            solver.visit(v, added_edge)
            # add_edge(tree, added_edge, weight)

            new_cost = average_pairwise_distance(tree)

            if new_cost < orig_cost:
                return optimize_additions(solver, tree, new_cost)
            else:
                solver.unvisit(v)

        # remove considered edge
        edges.remove(added_edge)
    return orig_cost


def optimize_removal(solver: GraphSolver, tree: Graph, orig_cost: float):
    candidates = [v for v in tree.nodes if not solver.is_required(v) and is_leaf(tree, v)]
    while candidates:
        print(candidates)
        # random.seed(0)
        node = random.choice(candidates)
        candidates.remove(node)
        edge = (node, list(tree.neighbors(node))[0])

        solver.unvisit(node)
        new_cost = average_pairwise_distance(tree)
        if new_cost < orig_cost:
            print('removed', node)
            return optimize_removal(solver, tree, new_cost)
        else:
            solver.add_edge(edge)
    return orig_cost


# Helper Functions
def kill_cycle(solver: GraphSolver, cycle: list, orig_cost: float):
    """
    Returns the first edge found in the cycle which, if removed from tree, leads to a decrease in cost (average pairwise
    distance).
    :param tree: tree (with 1 extra edge) to consider
    :param cycle: list of edges to consider (which form a cycle, removal of any restores tree)
    :param orig_cost: original cost
    :return:
    """
    tree = solver.T
    for edge in cycle:
        solver.remove_edge(edge)
        new_cost = average_pairwise_distance(tree)
        solver.add_edge(edge)
        if new_cost < orig_cost:
            return edge, new_cost

    return None, orig_cost


def is_leaf(graph: Graph, node: int):
    return len(list(graph.neighbors(node))) == 1
