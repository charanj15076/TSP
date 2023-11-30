import networkx as nx
import matplotlib.pyplot as plt

def christofides(G, pos, mapper_dict,weight="weight"):
    loop_nodes = nx.nodes_with_selfloops(G)
    try:
        node = next(loop_nodes)
    except StopIteration:
        pass
    else:
        G = G.copy()
        G.remove_edge(node, node)
        G.remove_edges_from((n, n) for n in loop_nodes)
    # Check that G is a complete graph
    N = len(G) - 1
    # This check ignores selfloops which is what we want here.
    if any(len(nbrdict) != N for n, nbrdict in G.adj.items()):
        raise nx.NetworkXError("G must be a complete graph.")
    
    tree = nx.minimum_spanning_tree(G, weight=weight)
    L = G.copy()
    L.remove_nodes_from([v for v, degree in tree.degree if not (degree % 2)])
    MG = nx.MultiGraph()
    MG.add_edges_from(tree.edges)
    edges = nx.min_weight_matching(L, weight=weight)
    MG.add_edges_from(edges)

    # find an Eulerian cycle of the multigraph
    initial_tour = list ( nx.eulerian_circuit(MG,source=0) )
    
    #Remove duplicate nodes in the path
    nodes = []
    for u, v in initial_tour:
        if v in nodes:
            continue
        if not nodes:
            nodes.append(u)
        nodes.append(v)
    nodes.append(nodes[0])
    
    edge_list = list(nx.utils.pairwise(nodes))

    # Draw closest edges on each node only
    nx.draw_networkx_edges(G, pos, edge_color="blue", width=0.5)

    # Draw the route
    nx.draw_networkx(
        G,
        pos,
        with_labels=True,
        edgelist=edge_list,
        edge_color="red",
        node_size=1000,
        width=3,
        arrows=True,
        arrowstyle= '-|>',
        labels=mapper_dict,
        
    )
    #plt.figure("Christofides")
    plt.title("The optimal path using Christofides")
    plt.show()
    return edge_list
