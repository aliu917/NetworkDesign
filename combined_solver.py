from graphsolver import GraphSolver
from graphsolver import weight
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
from simple_tests import test6
from optimizer import optimize
import opt_sorted_central_avg
import optimized_solver_1
import optimized_solver_1_sorted
import optimized_solver_1_sorted_allPaths
import opt_sorted_central_only
import opt_sorted_central_basic

def solve(G):
    ossort_T = opt_sorted_central_avg.solve(G)
    if average_pairwise_distance(ossort_T) == 0:
        return ossort_T
    os_T = optimized_solver_1.solve(G)
    osca_T = optimized_solver_1_sorted.solve(G)
    allPaths_T = optimized_solver_1_sorted_allPaths.solve(G)
    osco_T = opt_sorted_central_only.solve(G)
    oscb_T = opt_sorted_central_basic.solve(G)
    all_trees = [ossort_T, os_T, osca_T, allPaths_T, osco_T, oscb_T]
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
