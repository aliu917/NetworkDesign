import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gen cities.')
    parser.add_argument('--num_cities',  type=int, required=True)
    parser.add_argument('--map_size', type=int, required=True)
    args = parser.parse_args()

    # num_cities x num_cities array with max value map_size for each element
    # cities[0] is the position of city 0
    cities = np.random.random(np.full(args.num_cities, args.num_cities)) * args.map_size

    # Generate all edge possibilities
    city_nums = list(range(args.num_cities))
    print(city_nums)
    edge_possibilities = []
    for a in city_nums:
        print(a)
        for b in city_nums:
            if a < b:
                print(cities[a])
                print(cities)
                distance = np.linalg.norm(cities[a] - cities[b])
                edge_possibilities.append((a,b,distance))

    # Sample some edges to put in the list
    num_edges = np.random.randInt(args.num_cities - 1, args.num_cities * (args.num_cities - 1))
    edges = np.random.sample

    # Store in a .in file

