from collections import defaultdict

import networkx as nx
from collections import defaultdict
from os import makedirs
from os.path import join, isfile, dirname
import json


def is_valid_network(G, T):
    """
    Checks whether T is a valid network of G.
    Args:
        G: networkx.Graph
        T: networkx.Graph

    Returns:
        bool: whether T is a valid network
    """

    return nx.is_tree(T) and nx.is_dominating_set(G, T.nodes)


def average_pairwise_distance(T: nx.Graph):
    """
    Computes the average pairwise distance between vertices in T.
    This is what we want to minimize!

    Note that this function is a little naive, i.e. there are much
    faster ways to compute the average pairwise distance in a tree.
    Feel free to write your own!

    Args:
        T: networkx.Graph, a tree

    Returns:
        double: the average pairwise distance
    """
    if T.number_of_edges() == 0:
        return 0
    else:
        return nx.average_shortest_path_length(T, 'weight')
    # path_lengths = nx.all_pairs_dijkstra_path_length(T)
    # total_pairwise_distance = (
    #     sum([sum(length[1].values()) for length in path_lengths]) / 2
    # )
    # return total_pairwise_distance / (len(T) * (len(T) - 1))


def average_pairwise_distance_fast(T):
    """Calculates the average pairwise distance for a tree in linear time.

    Since there is always unique path between nodes in a tree, each edge in the
    tree is used in all of the paths from the connected component on one side
    of the tree to the other. So each edge contributes to the total pairwise cost
    in the following way: if the size of the connected components that are
    created from removing an edge e are A and B, then the total pairwise distance
    cost for an edge is 2 * A * B * w(e) = (# of paths that use that edge) * w(e).
    We multiply by two to consider both directions that paths can take on an
    undirected edge.

    Since each edge connects a subtree to the rest of a tree, we can run DFS
    to compute the sizes of all of the subtrees, and iterate through all the edges
    and sum the pairwise distance costs for each edge and divide by the total
    number of pairs.

    This is very similar to Q7 on MT1.

    h/t to Noah Kingdon for the algorithm.
    """
    if not nx.is_connected(T):
        raise ValueError("Tree must be connected")

    if len(T) == 1: return 0

    subtree_sizes = {}
    marked = defaultdict(bool)
    # store child parent relationships for each edge, because the components
    # created when removing an edge are the child subtree and the rest of the vertices

    root = list(T.nodes)[0];

    child_parent_pairs = [(root, root)]

    def calculate_subtree_sizes(u):
        """Iterates through the tree to compute all subtree sizes in linear time

        Args:
            u: the root of the subtree to start the DFS

        """
        unmarked_neighbors = filter(lambda v: not marked[v], T.neighbors(u))
        marked[u] = True
        size = 0
        for v in unmarked_neighbors:
            child_parent_pairs.append((v, u))
            calculate_subtree_sizes(v)
            size += subtree_sizes[v]
        subtree_sizes[u] = size + 1
        return subtree_sizes[u]

    calculate_subtree_sizes(root)  # any vertex can be the root of a tree

    cost = 0
    for c, p in child_parent_pairs:
        if c != p:
            a, b = subtree_sizes[c], len(T.nodes) - subtree_sizes[c]
            w = T[c][p]["weight"]
            cost += 2 * a * b * w
    return cost / (len(T) * (len(T) - 1))

class Cacher():
    def __init__(self, OUTPUT_DIRECTORY, cache_type="all"):
        self.NEVER_USE_CACHE_FILENAME = "never_use_cache.txt"
        self.OUTPUT_DIRECTORY = OUTPUT_DIRECTORY
        self.PREV_OUTPUTS_FILENAME = join(OUTPUT_DIRECTORY, 'all_prev_outputs.txt')
        from parse import write_output_file
        self.write_output_file = write_output_file
        assert cache_type == "all" or cache_type == "some" or cache_type == "none"
        self.cache_type = cache_type
        self.cache_exceptions = []
        if cache_type == "some":
            self.cache_exceptions = self.load_cache_exceptions()

        # Key: input filename
        # Value: {best: solver_filename, data: {solver_filename: {cost: x, time: x}}
        self.data = {}
        self.reload_cache()
        self.changes = []

    def load_cache_exceptions(self):
        if isfile(self.PREV_OUTPUTS_FILENAME):
            with open(self.NEVER_USE_CACHE_FILENAME, 'r') as f:
                return f.read().splitlines()
        else:
            print("WARNING: never_use_cache.txt not found")
            return []

    def reload_cache(self):
        if isfile(self.PREV_OUTPUTS_FILENAME):
            with open(self.PREV_OUTPUTS_FILENAME, 'r') as f:
                self.data = json.load(f)
        else:
            print("WARNING: No cached output found")
            self.data = {}

    def is_cached(self, input_filename, solver_filename):
        if self.cache_type == "none" or solver_filename in self.cache_exceptions:
            return False
        else:
            return self.is_cached_no_exceptions(input_filename, solver_filename)

    def is_cached_no_exceptions(self, input_filename, solver_filename):
        return input_filename in self.data.keys() \
                and solver_filename in self.data[input_filename]['data'].keys()

    def get_cost(self, input_filename, solver_filename):
        # Errors if is_cached_no_exceptions() would have returned False
        return self.data[input_filename]['data'][solver_filename]['cost']

    def get_runtime(self, input_filename, solver_filename):
        # Errors if is_cached_no_exceptions() would have returned False
        return self.data[input_filename]['data'][solver_filename]['runtime']

    def get_best_cost(self, input_filename, solver_filename):
        # Errors if is_cached_no_exceptions() would have returned False
        return self.data[input_filename]['data'][self.get_best_solver(input_filename)]['cost']

    def get_best_solver(self, input_filename):
        # Errors if is_cached_no_exceptions() would have returned False
        return self.data[input_filename]['best']

    def get_cache(self):
        return self.data

    def set_cache_type(self, cache_type):
        prev_cache_type, self.cache_type = self.cache_type, cache_type
        return prev_cache_type

    def cache_if_better_or_none(self, input_filename, solver_filename, cost, runtime, tree):
        # Update prev_outputs and .out only if a previous run was worse or it was never saved before
        out_file = join(self.OUTPUT_DIRECTORY, input_filename[:-3], solver_filename + '.out')
        if not isfile(out_file) or not self.is_cached_no_exceptions(input_filename, solver_filename) \
                or self.get_cost(input_filename, solver_filename) > cost:

            makedirs(dirname(out_file), exist_ok=True)
            self.write_output_file(tree, out_file)

            self.cache(input_filename, solver_filename, cost, runtime)

            if self.get_cost(input_filename, solver_filename) > cost:
                print('New best solver for {} is {} with cost {} and time {}' \
                        .format(input_filename, solver_filename, cost, runtime))

    def cache(self, input_filename, solver_filename, cost, runtime):
        self.changes.append((input_filename, solver_filename))
        if not input_filename in self.data.keys():
            self.data[input_filename] = {'best': solver_filename, 'data': {solver_filename:{'cost': cost, 'runtime': runtime}}}
            return
        
        self.data[input_filename]['data'][solver_filename] = {'cost': cost, 'runtime': runtime}
        if cost < self.get_best_cost(input_filename, solver_filename):
            self.data[input_filename]['best'] = solver_filename

    def override(self, data):
        if len(data.keys()) == 0:
            return self.data

        for input_filename, solver_filename in self.changes:
            if not input_filename in data.keys():
                data[input_filename] = {'best': solver_filename, 'data': 
                    {solver_filename:{'cost': self.get_cost(input_filename, solver_filename), 
                                      'runtime': self.get_runtime(input_filename, solver_filename)}}}
            else:
                if data[input_filename]['data'][data[input_filename]['best']]['cost'] \
                    > self.get_cost(input_filename, solver_filename):
                    data[input_filename]['best'] = solver_filename

                data[input_filename]['data'][solver_filename] = {'cost': self.get_cost(input_filename, solver_filename), 
                                          'runtime': self.get_runtime(input_filename, solver_filename)}

        return data
        
    def save(self):
        with open(self.PREV_OUTPUTS_FILENAME, 'w') as f:
            json.dump(self.data, f, indent=2)

    def save_data(self, data):
        with open(self.PREV_OUTPUTS_FILENAME, 'w') as f:
            json.dump(data, f, indent=2)
