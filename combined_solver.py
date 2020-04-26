from graphsolver import GraphSolver
from graphsolver import weight
from utils import average_pairwise_distance
from optimizer_sorted import optimize_sorted, kill_cycle
from simple_tests import test6
from optimizer import optimize
# import opt_sorted_central_avg
# import optimized_solver_1
# import optimized_solver_1_sorted
# import optimized_solver_1_sorted_allPaths
# import opt_sorted_central_only
# import opt_sorted_central_basic
# import betweenness_solver
# import shortest_path_solver
from runner import saved_costs
from multiprocessing import Pool

from importlib import import_module
from parse import read_output_file
from os.path import join

solver_filenames = [
        'opt_sorted_central_avg',
        'optimized_solver_1',
        'optimized_solver_1_sorted',
        'optimized_solver_1_sorted_allPaths',
        'opt_sorted_central_only',
        'opt_sorted_central_basic',
        'betweenness_solver',
        'shortest_path_solver'
    ]

cacher = None # sketchily give this module a cacher object later if you want the speedup
PREV_OUTPUTS_FILENAME = None # This too
input_filename = None # This too

def solve(G):
    global saved_costs, solver_filenames

    g = GraphSolver(G)
    for v in list(g.G.nodes):
        if len(list(g.neighbors(v))) == g.n - 1:  # Special case when one vertex is connected to all of them
            g.visit(v)
            return g.T

    solvers = [import_module(solver_filename) for solver_filename in solver_filenames]
    skipped_costs = []
    skipped_solvers = []

    # Don't calculate for inputs we already know costs for deterministically
    if cacher is not None:
        skip = []
        for i in range(len(solvers)):
            if getattr(solvers[i], 'isDeterministic', False) and cacher.is_cached(input_filename, solver_filenames[i]):
                skipped_costs.append(cacher.get_cost(input_filename, solver_filenames[i]))
                skip.append(i)
                skipped_solvers.append(solver_filenames[i])
        solver_filenames = [f for i, f in enumerate(solver_filenames) if i not in skip]
        solvers = [s for i, s in enumerate(solvers) if i not in skip]
    else:
        print('WARNING: Cacher object not given to combined_solver. Not using cache')

    ############### Parallelizing ########################
    pool = Pool(len(solvers))

    async_solvers = [pool.apply_async(solver.solve, [G]) for solver in solvers]
    trees = [async_solver.get(1000000000) for async_solver in async_solvers]

    pool.close()
    pool.join()


    ################ Non - parallelizing ####################

    # trees = [solver.solve(G) for solver in solvers]

    #########################################################

    # Cache costs
    costs = [average_pairwise_distance(t) for t in trees]
    if cacher is not None:
        for i in range(len(trees)):
            cacher.cache_if_better_or_none(input_filename, solver_filenames[i], costs[i], None, trees[i])

    # Create lists with the same length
    all_trees = [None] * len(skipped_costs) + trees
    all_costs = skipped_costs + costs
    solver_filenames = skipped_solvers + solver_filenames

    # Sort
    all_trees = [tree for c, tree in sorted(zip(all_costs, all_trees), key=lambda pair: pair[0])]
    solver_filenames = [filename for c, filename in sorted(zip(all_costs, solver_filenames), key=lambda pair: pair[0])]
    all_costs = sorted(all_costs)

    # Print saved costs
    second_smallest = sorted(all_costs)[1]
    individual_saved_costs = [second_smallest - cost if second_smallest - cost > 0 else 0 for cost in all_costs]
    saved_costs = [sum(x) for x in zip(saved_costs, individual_saved_costs)]
    print(saved_costs)

    # Get the tree to return
    min_tree = all_trees[0]
    if min_tree is None:
        out_file = join(OUTPUT_DIRECTORY, input_filename[:-3], solver_filenames[0] + '.out')
        min_tree = read_output_file(out_file, G)

    return min_tree

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
