import random
from queue import PriorityQueue

import networkx as nx
import numpy as np

from disjoint_set import DisjointSet


# Gets the weight of specified edge
def weight(G, e):
    edge_dict = G.get_edge_data(e[0], e[1])
    return edge_dict["weight"]

class Graph:

    def __init__(self, G):
        n = len(G.nodes)
        self.n = n
        self.G = G
        self.required = n * [False]
        self.optional = n * [False]
        self.all_visited = n * [False]
        self.dj_set = DisjointSet(n)
        self.T = nx.Graph()

    def nodes(self):
        return self.G.nodes

    def edges(self):
        return self.G.nodes

    def is_required(self, x):
        return self.required[x]

    def neighbors(self, v):
        return self.G.neighbors(v)

    def is_optional(self, x):
        return self.optional[x]

    # Finds the minimum edge in edges list or returns 0 if no elements in edges
    def minEdge(self, edges):
        if edges:
            return min(edges)
        return 0

    def edges(self, v):
        return self.G.edges(v)

    # Finds the minimum edge weight of all of u's outoing edges except for the edge (u,v)
    def minEdgeWeight(self, u, v):
        return Graph.minEdge(self, [weight(self.G, e) for e in list(self.edges(u)) if e[0] != v and e[1] != v])

    # Heuristic helper to approximate number of nodes left to visit
    def nodes_left(self):
        return self.n - np.count_nonzero([sum(x) for x in zip(self.optional, self.all_visited)]) + 1

    # Adds vertex v to T and assigns neighbors to optional visiting
    def visit(self, v, edge=None, optionals=True):
        self.all_visited[v] = True
        self.required[v] = True
        self.optional[v] = False
        self.dj_set.makeSet(v)
        self.T.add_node(v)
        if edge:
            self.T.add_edge(edge[0], edge[1], weight=weight(self.G, edge))
            self.dj_set.union(edge[0], edge[1])
        if optionals:
            for u in list(self.neighbors(v)):
                if not self.required[u]:
                    self.optional[u] = True

    # Helper for finding all leaf paths -- Traverses each leaf path to trim off non-cycle elements
    def traverse_path(self, v, add_v, visited, prevV):
        if visited[v]:
            return
        visited[v] = True
        self.all_visited[v] = True
        if add_v:
            if prevV != -1:
                self.visit(v, (v, prevV), False)
            else:
                self.visit(v, None, False)
            if len(list(self.neighbors(v))) > 2:
                for u in list(self.neighbors(v)):
                    self.optional[u] = True
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

    def surrounded(self, v):
        for u in list(self.neighbors(v)):
            if not self.required[u] and not self.optional[u]:
                return False
        return True

    def default_heuristic(self, g, u, v):
        return weight(self.G, (u, v))

    # Initializes the pq with beginning elements
    def initialize_pq(self, q, h):
        for i in range(len(self.required)):
            if self.required[i]:
                for u in list(self.neighbors(i)):
                    if not self.all_visited[u]:
                        q.put((-h(self, u, i), (u, i)))

    # Solve helper to greedily find next optimal edge according to heuristic and add it
    def dijkstra_solve_graph(self, start_v=None, h=None, first_h=None):
        if not h:
            h = lambda g, u, v: self.default_heuristic(self, u, v)
        q = PriorityQueue()
        if not any(self.required):
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
            # print(T.nodes)
            # print("Calculating heuristics after visiting", v)
            for u in list(self.neighbors(v)):
                if not self.all_visited[u]:
                    q.put((-h(self, u, v), (u, v)))
        # print(self.required)
        # print(self.T.nodes)
        # print(self.T.edges)
        return self.T
