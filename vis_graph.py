from parse import read_output_file_unsafe, read_input_file
import networkx as nx
import matplotlib.pyplot as plt
import argparse

# Example: 
# python3.7 vis_graph.py --input our_inputs/25/1586412046.5950363.in --output our_outputs/25/1586412046.5950363/optimized_solver_1_sorted.out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='vis graph')
    parser.add_argument('--input', type=str, required=True, help='path to .in file')
    parser.add_argument('--output', type=str, required=True, help='path to .out file')
    args = parser.parse_args()

    G_in = read_input_file(args.input, max_size=100)
    # Don't check if the graph is valid when reading it in
    G_out = read_output_file_unsafe(args.output)


    overlap_edges = set()
    diff_edges = set()
    for e in G_in.edges:
        if e in G_out.edges:
            overlap_edges.add(e)
        else:
            diff_edges.add(e)

    overlap_v = set()
    diff_v = set()
    neighbor_v = set()
    neighbor_edges = set()
    for v in G_in.nodes:
        if v in G_out.nodes:
            overlap_v.add(v)
            neighbors = list(G_in.neighbors(v))
            neighbor_v.update(neighbors)
            neighbor_edges.update([(v,n) for n in neighbors])
        else:
            diff_v.add(v)
    # precedence is solution > neighbors > difference
    for v in G_out.nodes:
        if v in neighbor_v:
            neighbor_v.remove(v)
    for v in neighbor_v:
        if v in diff_v:
            diff_v.remove(v)
    # Same for edges
    for e in G_out.edges:
        if e in neighbor_edges:
            neighbor_edges.remove(e)
        if (e[1], e[0]) in neighbor_edges:
            neighbor_edges.remove((e[1], e[0]))
    for e in neighbor_edges:
        if e in diff_edges:
            diff_edges.remove(e)
        if (e[1], e[0]) in diff_edges:
            diff_edges.remove((e[1], e[0]))



    # overlap_v, overlap_edges, diff_v, diff_edges, neighbor_v, neighbor_edges = \
    #     list(overlap)

    pos = nx.spring_layout(G_in, seed=1)  # positions for all nodes

    nx.draw_networkx_nodes(G_in, pos, nodelist=diff_v, node_color='g', alpha=0.8)
    nx.draw_networkx_nodes(G_in, pos, nodelist=neighbor_v, node_color='g', alpha=0.8)
    nx.draw_networkx_nodes(G_in, pos, nodelist=overlap_v, node_color='b', alpha=0.8)

    nx.draw_networkx_edges(G_in, pos, edgelist=diff_edges, width=1, alpha=0.5, edge_color='r')
    nx.draw_networkx_edges(G_in, pos, edgelist=neighbor_edges, width=1, alpha=0.5, edge_color='g')
    nx.draw_networkx_edges(G_in, pos, edgelist=overlap_edges, width=2, alpha=0.8, edge_color='b')

    labels = {}
    for v in G_in.nodes:
        labels[v] = r'${}$'.format(v)
    nx.draw_networkx_labels(G_in, pos, labels, font_size=12)

    edge_labels = nx.get_edge_attributes(G_in,'weight')
    keys = list(edge_labels.keys())
    for k in keys:
        if G_out.edges.get(k, None) is None:
            del edge_labels[k]
    nx.draw_networkx_edge_labels(G_in,pos,edge_labels=edge_labels, font_size=7)

    print('Blue = node/edge in the solution graph')
    print('Green = node/edge of a neighbor of nodes in solution graph')
    print('Red = node/edge in the input graph but not in the solution graph')

    plt.title(args.output)
    plt.show()
