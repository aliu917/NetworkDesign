import argparse
import sys
import time
from pathlib import Path

import numpy as np


def all_connected(num_cities, edges):
    visited = np.array([False] * num_cities)
    dfs(0, edges, visited)
    return np.all(visited)


def dfs(v, edges, visited):
    visited[v] = True
    for u in edges[v]:
        if not visited[u]:
            dfs(u, edges, visited)


def add_edges(edges):
    possible_num_edges = args.num_cities * (args.num_cities - 1) // 2
    num_edges = int(np.random.random() * (possible_num_edges + 1))  # inclusive
    for i in range(num_edges):
        a = np.random.choice(args.num_cities)
        b = np.random.choice(args.num_cities)
        if a > b:
            a, b = b, a
        if a != b and b not in edges[a]:
            edges[a].append(b)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gen cities.')
    parser.add_argument('--num_cities', type=int, required=True)
    parser.add_argument('--map_size', type=int, default=100)
    args = parser.parse_args()

    # set city_rank, the folder to put this data file in
    if args.num_cities > 100:
        print('num cities > 100. Aborting')
        sys.exit()
    elif args.num_cities > 50:
        city_rank = 100
    elif args.num_cities > 25:
        city_rank = 50
    elif args.num_cities > 0:
        city_rank = 25
    else:
        print('num cities <= 0. Aborting')
        sys.exit()

    if args.map_size <= 0 or args.map_size > 100:
        print('map size not in (0, 100]. Aborting')
        # Random number generation doesn't include the upper bound
        sys.exit()

    # Sample more edges until all vertices are included
    edges = {}
    for a in range(args.num_cities):
        edges[a] = []

    add_edges(edges)

    while not all_connected(args.num_cities, edges):
        add_edges(edges)

    # Make the folder
    foldername = "./our_inputs/" + str(city_rank) + '/'
    Path(foldername).mkdir(parents=True, exist_ok=True)

    # Store in a .in file
    filename = str(time.time()) + ".in"
    f = open(foldername + filename, "w")

    f.write(str(args.num_cities) + '\n')
    for v in edges.keys():
        for u in edges[v]:
            # Flip order randomly
            if np.random.random() < 0.5:
                f.write(str(int(v)) + " " + str(int(u)) + " " + ("%.3f" % (np.random.random() * args.map_size)) + "\n")
            else:
                f.write(str(int(u)) + " " + str(int(v)) + " " + ("%.3f" % (np.random.random() * args.map_size)) + "\n")
    f.close()
