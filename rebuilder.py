"""
Implementation of rebuild, which takes a GraphSolver and removes a specified proportion of nodes from its tree.
"""
from networkx import Graph

from graphsolver import GraphSolver
from utils import average_pairwise_distance
import random


class Rebuilder:
    ATTEMPT_LIMIT = 100  # the number of attempts to make before we consider a local minimum to be found
    RESET_ETA = .5  # learning rate when local min is found
    MIN_REMOVAL = 3  # minimum number of nodes to remove
    A = .08  # values of a in eta calculation: x/(x+a); larger A mean sharper incline

    solver: GraphSolver
    attempts: int
    local_min: float
    cost: float

    def __init__(self, solver: GraphSolver):
        self.solver = solver
        self.attempts = 0
        self.local_min = average_pairwise_distance(solver.T)
        self.cost = self.local_min

    def rebuild(self):
        """
        Removes a proportion of nodes in solver.T, based on momentum
        """
        # housekeeping
        self.attempts += 1
        self.cost = average_pairwise_distance(self.solver.T)

        # compute number of nodes to remove
        n = self.solver.T.number_of_nodes()
        if self.attempts >= self.ATTEMPT_LIMIT:
            r = self.RESET_ETA * n
        else:
            r = min(self.MIN_REMOVAL, n * self.calc_eta())

        # remove nodes
        for v in self.BFS(self.solver.T, r):
            self.solver.unvisit(v)

        self.local_min = min(self.local_min, self.cost)

    def calc_eta(self):
        """
        Calculates eta (proportion of nodes to remove) based on diff.
        :return: eta in [0,1)
        """
        diff = abs(self.local_min - self.cost) / self.local_min
        return diff / (diff + self.A)

    def BFS(self, tree: Graph, num_nodes):
        """
        Runs BFS on tree to find num_nodes nodes
        :param tree: tree on which to search
        :param num_nodes: number of nodes to return
        :return: list containing the first num_nodes found, removal from tree should maintain tree property
        """

        leaves = [v for v in tree.nodes if tree.neighbors(v) == 1]
        num_visited = 0
        q = [random.choice(leaves)]
        nodes = []
        while q and num_visited < num_nodes:
            v = q.pop(0)
            nodes.append(v)
            num_nodes += 1
            for neighbor in tree.neighbors(v):
                if neighbor not in nodes:
                    q.append(neighbor)
        return nodes
