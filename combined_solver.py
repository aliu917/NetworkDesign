from graphsolver import GraphSolver
from graphsolver import weight
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
from simple_tests import test6
from optimizer import optimize
import opt_sorted_h1
import optimized_solver_1
import optimized_solver_1_sorted
import optimized_solver_1_sorted_allPaths

def solve(G):
    ossort_T = opt_sorted_h1.solve(G)
    os_T = optimized_solver_1.solve(G)
    osh1_T = optimized_solver_1_sorted.solve(G)
    allPaths_T = optimized_solver_1_sorted_allPaths.solve(G)
    all_trees = [ossort_T, os_T, osh1_T, allPaths_T]
    costs = [average_pairwise_distance(t) for t in all_trees]
    costs.sort()
    all_trees.sort(key=lambda t: average_pairwise_distance(t))
    return all_trees[0]

# test6(solve)


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')
