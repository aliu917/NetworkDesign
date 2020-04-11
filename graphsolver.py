import random
from queue import PriorityQueue

import networkx as nx
import numpy as np

from unused.disjoint_set import DisjointSet


# Gets the weight of specified edge
def weight(G, e):
    edge_dict = G.get_edge_data(e[0], e[1])
    return edge_dict["weight"]

def is_leaf(G, v):
    return len(list(G.neighbors(v))) == 1

def edge_exists(lst, e):
    return e in lst or (e[1], e[0]) in lst


class GraphSolver:

    def __init__(self, G):
        n = len(G.nodes)
        self.n = n
        self.G = G
        self.in_tree = n * [False]
        self.optional = n * [0]
        self.all_visited = n * [False]
        self.dj_set = DisjointSet(n)
        self.T = nx.Graph()

    def nodes(self):
        return self.G.nodes

    # Returns whether the vertex x is in the tree
    def is_in_tree(self, x):
        return self.in_tree[x]

    # Gets all neighbors of v (NOTE: doesn't return a list, so must cast it as list(g.neighbors(v)))
    def neighbors(self, v):
        return self.G.neighbors(v)

    # Determines whether x is already dominated (aka. we don't need to add it to the tree)
    def is_optional(self, x):
        return self.optional[x] > 0

    # Dtermines whether x is an extra vertex (required) or one that can be removed and keep tree valid
    def is_required(self, x):
        return not all([self.optional[u] > 1 for u in list(self.neighbors(x)) if not self.in_tree[u]])

    # Finds the minimum edge in edges list or returns 0 if no elements in edges
    def minEdge(self, edges):
        if edges:
            return min(edges)
        return 0

    #Gets all edges adjacent to v (if given) or all edges in the graph if not
    def edges(self, v=-1):
        if v < 0:
            return self.G.edges
        return self.G.edges(v)

    # Finds the minimum edge weight of all of u's outoing edges except for the edge (u,v)
    def minEdgeWeight(self, u, v):
        return GraphSolver.minEdge(self, [weight(self.G, e) for e in list(self.edges(u)) if e[0] != v and e[1] != v])

    # Heuristic helper to approximate number of nodes left to visit
    def nodes_left(self):
        return self.n - np.count_nonzero([sum(x) for x in zip(self.optional, self.all_visited)]) + 1

    # Adds vertex v to T and assigns neighbors to optional visiting
    def visit(self, v, edge=None, optionals=True):
        if (self.in_tree[v]):
            print("Attempting to add vertex", v, "which is already present.")
            return
        self.all_visited[v] = True
        self.in_tree[v] = True
        self.optional[v] = 0
        self.T.add_node(v)
        if edge:
            self.T.add_edge(edge[0], edge[1], weight=weight(self.G, edge))
            # self.dj_set.union(edge[0], edge[1])
        for u in list(self.neighbors(v)):
            if optionals:
                if not self.in_tree[u]:
                    self.optional[u] += 1

    # Removes vertex v from T
    def unvisit(self, v):
        if (not self.in_tree[v]):
            print("Attempting to remove vertex", v, "which is not in tree.")
            return
        self.T.remove_node(v)
        self.all_visited[v] = False
        self.in_tree[v] = False
        self.optional[v] = 0
        for u in list(self.neighbors(v)):
            if (self.in_tree[u]):
                self.optional[v] += 1
            else:
                self.optional[u] = max(0, self.optional[u - 1])

    # Removes edge e from T
    def remove_edge(self, e):
        assert self.in_tree[e[0]] and self.in_tree[e[1]], "Cannot remove edge (" + str(e[0]) + ", " + str(e[1]) + ") not in tree"
        if is_leaf(self.G, e[0]) and is_leaf(self.G, e[1]):
            print("Cannot remove edge", e, "connecting two leaves")
        if is_leaf(self.G, e[0]):
            self.unvisit(e[0])
        elif is_leaf(self.G, e[1]):
            self.unvisit(e[1])
        else:
            self.T.remove_edge(e[0], e[1])

    # Adds edge e to T
    def add_edge(self, e):
        assert self.in_tree[e[0]] or self.in_tree[e[1]], "Cannot add disconnected edge (" + str(e[0]) + ", " + str(e[1]) + ")"
        if not self.in_tree[e[0]]:
            self.visit(e[0], e)
        elif not self.in_tree[e[1]]:
            self.visit(e[1], e)
        else:
            self.T.add_edge(e[0], e[1], weight=weight(self.G, e))

    # Helper for finding all leaf paths -- Traverses each leaf path to trim off non-cycle elements
    def traverse_path(self, v, add_v, visited, prevV):
        if visited[v]:
            return
        visited[v] = True
        self.all_visited[v] = True
        if add_v:
            if prevV != -1:
                self.visit(v, (v, prevV))
            else:
                self.visit(v, None)
            if len(list(self.neighbors(v))) > 2:
                return v
            else:
                for adj in list(self.neighbors(v)):
                    return self.traverse_path(adj, True, visited, v)
        else:
            return self.traverse_path(list(self.neighbors(v))[0], True, visited, -1)

    # Finds all leaf paths in G and sets all vertices in path to visited
    def find_leaf_path(self):
        leaves = [v for v in self.nodes() if len(list(self.neighbors(v))) == 1]
        if not leaves:
            return
        visited = len(list(self.nodes())) * [False]
        # for leaf in leaves:
        #     visited = len(list(G.nodes)) * [False]
        #     traverse_path(leaf, False, visited, None)
        return self.traverse_path(leaves[0], False, visited, None)

    #Determines whether v is surrounded or not
    def surrounded(self, v):
        for u in list(self.neighbors(v)):
            if not self.all_visited[u] and not self.optional[u]:
                return False
        return True

    # Default heuristic equivalent to mst
    def default_heuristic(self, g, u, v):
        return weight(self.G, (u, v))

    # Initializes the pq with beginning elements
    def initialize_pq(self, q, h):
        for i in range(self.n):
            if self.in_tree[i]:
                for u in list(self.neighbors(i)):
                    if not self.all_visited[u]:
                        q.put((-h(self, u, i), (u, i)))

    # Solve helper to greedily find next optimal edge according to heuristic and add it
    def dijkstra_solve_graph(self, start_v=None, h=None, first_h=None):
        if not h:
            h = lambda g, u, v: self.default_heuristic(self, u, v)
        q = PriorityQueue()
        if not any(self.in_tree):
            # random.seed(0)
            chosenV = random.randint(0, self.n - 1)
            if start_v:
                chosenV = start_v
            elif first_h:
                chosenV = first_h(self)
            self.visit(chosenV)
        self.initialize_pq(q, h)
        while q:
            e = q.get()[1]
            v = e[0]
            if np.count_nonzero([sum(x) for x in zip(self.optional, self.all_visited)]) == self.n:
                break
            if self.all_visited[v] or self.surrounded(v):
                continue
            self.visit(v, e)
            # print(self.T.nodes)
            # print("Calculating heuristics after visiting", v)
            for u in list(self.neighbors(v)):
                if not self.all_visited[u]:
                    q.put((-h(self, u, v), (u, v)))
        # print(self.in_tree)
        # print(self.T.nodes)
        # print(self.T.edges)
        return self.T
