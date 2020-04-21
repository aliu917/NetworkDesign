"""
Takes a graph and corresponding valid tree and optimizes cost by making three types of adjustments: adding an edge
(and a vertex, removing an (optional) edge (and vertex, or replacing an edge (while keeping same vertices). Runs
until no immediate changes lead to improvements.
"""
import random

from networkx import Graph, find_cycle, closeness_centrality, all_pairs_dijkstra

from graphsolver import GraphSolver
from utils import average_pairwise_distance, is_valid_network
from graphsolver import edge_exists, weight
from numpy import argmin

def optimize_sorted(solver: GraphSolver, tree: Graph, cycle_killer_fn, orig_cost: float = None):
    # noinspection PyUnusedLocal
    no_add = no_remove = no_cycle = False

    new_cost = optimize_cycle_remover(solver, tree, cycle_killer_fn, orig_cost)
    no_cycle = new_cost == orig_cost
    orig_cost = new_cost

    new_cost = optimize_additions_sorted(solver, tree, orig_cost)
    no_add = new_cost == orig_cost
    orig_cost = new_cost

    new_cost = optimize_removal_sorted(solver, tree, new_cost)
    no_remove = new_cost == orig_cost

    if no_add and no_remove and no_cycle:
        return

    optimize_sorted(solver, tree, cycle_killer_fn, orig_cost=new_cost)


def optimize_cycle_remover(solver, tree, cycle_killer_fn, orig_cost):
    if not orig_cost:
        orig_cost = average_pairwise_distance(tree)
    tree_set = set(tree.nodes)
    candidates = [(v, list(set(solver.neighbors(v)) & tree_set)) for v in solver.G if solver.is_optional(v) and len(set(solver.neighbors(v)) & tree_set) > 2]
    # Candidates contains all vertices with >2 neighbors in tree and list of all those neighboring vertices
    min_cost = orig_cost
    for pair in candidates:
        v = pair[0]
        edges = [(v,x) for x in pair[1] if weight(solver.G, (v,x)) < solver.max_T_edge_weight]
        if len(edges) < 2:
            continue
        edges.sort(key=lambda x: weight(solver.G, x))

        # Try adding a vertex and two edges to tree to make a cycle and delete min edge
        added_edge = False
        min_edge = edges[0]
        solver.add_edge(min_edge)
        for j in range(1, len(edges)):
            solver.add_edge(edges[j])

            cycle: list = find_cycle(tree, v)
            replaced_edge, new_cost = cycle_killer_fn(solver, cycle, orig_cost=min_cost)
            if replaced_edge:
                added_edge = True
                # print("Added vertex", v, "and edges:", min_edge, edges[j])
                # print("Prev cost:", min_cost)
                # print("New cost:", new_cost)
                min_cost = new_cost
                solver.remove_edge(replaced_edge)
            else:
                solver.remove_edge(edges[j])
        if not added_edge:
            solver.remove_edge(min_edge)
    return min_cost




def insertion_sort(edges, edge, solver):
    for i in range(len(edges)):
        if weight(solver.G, edge) < weight(solver.G, edges[i]):
            edges.insert(i, edge)
            break

def add_neighbors(solver, edges, v, sorted=False):
    for neighbor in solver.neighbors(v):
        if not edge_exists(solver.T.edges, (v, neighbor)) and not edge_exists(edges, (v, neighbor)):
            if sorted:
                insertion_sort(edges, (v,neighbor), solver)
            else:
                edges.append((v, neighbor))


def optimize_additions_sorted(solver: GraphSolver, tree: Graph, orig_cost: float = None):
    global edge_weights_dict
    graph = solver.G
    if orig_cost is None:
        orig_cost = average_pairwise_distance(tree)

    # get all edges to consider
    edges = []
    for node in tree.nodes:
        for neighbor in graph.neighbors(node):
            if not edge_exists(tree.edges, (node, neighbor)) and not edge_exists(edges, (node, neighbor)):
                edges.append((node, neighbor))

    # for each edge (consider order randomly)
    edges.sort(key=lambda x: weight(solver.G, x))
    while edges:
        # random.seed(0)
        # added_edge = random.choice(edges)
        # edges.remove(added_edge)
        added_edge = edges.pop(0)
        # print("Considering edge:", added_edge)
        # if added edge creates a cycle
        if added_edge[1] in tree.nodes:
            solver.add_edge(added_edge)
            while(True):
                try:
                    cycle: list = find_cycle(tree, added_edge[0])
                except:     #No cycle
                    break

                try:
                    cycle.remove(added_edge)
                except ValueError:
                    cycle.remove(added_edge[::-1])

                replaced_edge, new_cost = kill_cycle(solver, cycle, orig_cost)
                # print("replaced_edge:", replaced_edge)
                # print("cost:", new_cost)

                if replaced_edge:
                    orig_cost = new_cost
                    solver.remove_edge(replaced_edge)
                else:
                    solver.remove_edge(added_edge)
        # if other vertex not in tree
        else:
            v = added_edge[1]
            solver.visit(v, added_edge)
            # add_edge(tree, added_edge, weight)

            new_cost = average_pairwise_distance(tree)

            if new_cost < orig_cost:
                # print("added edge:", added_edge, "with vertex:", v)
                orig_cost = new_cost
                add_neighbors(solver, edges, v, True)
            else:
                solver.unvisit(v)

        # remove considered edge
    return orig_cost


def optimize_removal_sorted(solver: GraphSolver, tree: Graph, orig_cost: float):
    candidates = [v for v in tree.nodes if not solver.is_required(v) and is_leaf(tree, v)]
    while candidates:
        # print(candidates)
        # random.seed(0)
        candidates.sort(key=lambda x: closeness_centrality(solver.T, x))
        node = candidates.pop(0)
        edge = (node, list(tree.neighbors(node))[0])

        solver.unvisit(node)
        new_cost = average_pairwise_distance(tree)
        if new_cost < orig_cost:
            # print('removed', node)
            return optimize_removal_sorted(solver, tree, new_cost)
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
    min_edge = None
    for edge in cycle:
        solver.remove_edge(edge)
        new_cost = average_pairwise_distance(tree)
        still_valid = is_valid_network(solver.G, solver.T)
        solver.add_edge(edge)
        if new_cost < orig_cost and still_valid:
            min_edge = edge
            orig_cost = new_cost

    return min_edge, orig_cost

def kill_cycle_all_paths(solver: GraphSolver, cycle: list, orig_cost: float):
    """
    Returns the first edge found in the cycle which, if removed from tree, leads to a decrease in cost (average pairwise
    distance).
    :param tree: tree (with 1 extra edge) to consider
    :param cycle: list of edges to consider (which form a cycle, removal of any restores tree)
    :param orig_cost: original cost
    :return:
    """
    tree = solver.T

    weights = [0] * len(cycle)

    # Count the number of times each edge in the cycle appears in the paths
    for n, (dist, path) in all_pairs_dijkstra(solver.G):
        for target in path.keys():
            for v in range(1, len(path[target])):
                path_edge = (path[target][v-1], path[target][v])
                if path_edge in cycle:
                    weights[cycle.index(path_edge)] += 1

    # Multiply by the edge weight to get the contributing weight
    weights = [weights[i] * weight(solver.G, cycle[i]) for i in range(len(weights))]


    edge = cycle[argmin(weights)]
    print('weights for', cycle, 'are', weights)
    # cycle.sort(key= lambda x: weight(solver.T, x), reverse = True)
    # edge = cycle[0]
    solver.remove_edge(edge)
    new_cost = average_pairwise_distance(tree)
    solver.add_edge(edge)
    if new_cost < orig_cost:
        print('nice')
        return edge, new_cost
    else:
        # print('removing', edge, 'from cycle', cycle, "didn't decrease cost because", new_cost, '>=', orig_cost)
        # print(weight(solver.T, edge), 'from', [weight(solver.T, e) for e in cycle])
        pass
    return None, orig_cost


def is_leaf(graph: Graph, node: int):
    return len(list(graph.neighbors(node))) == 1
