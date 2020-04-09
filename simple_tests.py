import networkx as nx


def test(f):
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8])
    G.add_edge(0, 1, weight=1)
    G.add_edge(1, 2, weight=2)
    G.add_edge(0, 2, weight=1)
    G.add_edge(0, 3, weight=3)
    G.add_edge(3, 4, weight=5)
    G.add_edge(4, 5, weight=2)
    G.add_edge(3, 5, weight=4)
    G.add_edge(0, 6, weight=3)
    G.add_edge(0, 7, weight=2)
    G.add_edge(7, 8, weight=3)
    f(G)


def test2(f):
    print("test 2: center weights 2 outer weights 1")
    print("should be center vertex and 6")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edge(0, 1, weight=2)
    G.add_edge(0, 2, weight=2)
    G.add_edge(0, 3, weight=2)
    G.add_edge(0, 4, weight=2)
    G.add_edge(0, 5, weight=2)
    G.add_edge(0, 6, weight=2)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    G.add_edge(6, 7, weight=1)
    f(G)
    print()
    test2_1(f)


def test2_1(f):
    print("test 2-1: center weights 4 outside weights 1")
    print("Should be not center vertex")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edge(0, 1, weight=4)
    G.add_edge(0, 2, weight=4)
    G.add_edge(0, 3, weight=4)
    G.add_edge(0, 4, weight=4)
    G.add_edge(0, 5, weight=4)
    G.add_edge(0, 6, weight=4)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    G.add_edge(6, 7, weight=1)
    f(G)
    print()
    test2_2(f)

def test2_2(f):
    print("test 2-2: center weights 3 outside weights 1")
    print("Should be center vertex")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edge(0, 1, weight=3)
    G.add_edge(0, 2, weight=3)
    G.add_edge(0, 3, weight=3)
    G.add_edge(0, 4, weight=3)
    G.add_edge(0, 5, weight=3)
    G.add_edge(0, 6, weight=3)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    G.add_edge(6, 7, weight=1)
    f(G)
    print()
    test2_3(f)


def test2_3(f):
    # TODO: This part fails because edge weight 10 dominates and having more edge 1 weights
    # TODO: is better. Will probably need to fix these issues in the refining process...
    print("test 2-3: center weights 2 outside weights 1 but added 10 edge")
    print("Should be not center vertex")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8])
    G.add_edge(0, 1, weight=2)
    G.add_edge(0, 2, weight=2)
    G.add_edge(0, 3, weight=2)
    G.add_edge(0, 4, weight=2)
    G.add_edge(0, 5, weight=2)
    G.add_edge(0, 6, weight=2)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    G.add_edge(6, 7, weight=1)
    G.add_edge(7, 8, weight=10)
    f(G)


def test3(f):
    print("test 3: center connected to all vertices")
    print("should be only center vertex")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
    G.add_edge(0, 1, weight=2)
    G.add_edge(0, 2, weight=2)
    G.add_edge(0, 3, weight=2)
    G.add_edge(0, 4, weight=2)
    G.add_edge(0, 5, weight=2)
    G.add_edge(0, 6, weight=2)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    f(G)


def test4(f):
    print("test 4: Some random circular thing")
    print("should be 2 and 3")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4])
    G.add_edge(0, 1, weight=1)
    G.add_edge(0, 2, weight=3)
    G.add_edge(1, 3, weight=2)
    G.add_edge(2, 3, weight=1)
    G.add_edge(1, 4, weight=3)
    G.add_edge(2, 4, weight=2)
    G.add_edge(3, 4, weight=5)
    f(G)


def test5(f):
    print("Testing possible disconnect")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8])
    G.add_edge(0, 1, weight=2)
    G.add_edge(0, 2, weight=2)
    G.add_edge(0, 3, weight=2)
    G.add_edge(0, 4, weight=2)
    G.add_edge(0, 5, weight=2)
    G.add_edge(0, 6, weight=2)
    G.add_edge(1, 2, weight=1)
    G.add_edge(2, 3, weight=1)
    G.add_edge(3, 4, weight=1)
    G.add_edge(4, 5, weight=1)
    G.add_edge(5, 6, weight=1)
    G.add_edge(6, 1, weight=1)
    G.add_edge(6, 7, weight=1)
    G.add_edge(3, 8, weight=1)
    f(G)

def run_all_tests(f):
    test(f)
    print()
    test2(f)
    print()
    test3(f)
    print()
    test4(f)
    print()
    test5(f)
