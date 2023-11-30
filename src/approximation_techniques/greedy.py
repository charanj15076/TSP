import networkx as nx
import matplotlib.pyplot as plt

def greedy(G, pos, mapper_dict,weight="weight"):
    N = len(G)-1
    # This check ignores selfloops which is what we want here.
    if any(len(nbrdict) - (n in nbrdict) != N for n, nbrdict in G.adj.items()):
        raise nx.NetworkXError("G must be a complete graph.")

    source = nx.utils.arbitrary_element(G)
    
    if G.number_of_nodes() == 2:
        neighbor = next(G.neighbors(source))
        return [source, neighbor, source]

    nodeset = set(G)
    nodeset.remove(source)
    cycle = [source]
    next_node = source
    while nodeset:
        nbrdict = G[next_node]
        next_node = min(nodeset, key=lambda n: nbrdict[n].get(weight, 1))
        cycle.append(next_node)
        nodeset.remove(next_node)
    cycle.append(cycle[0])

    edge_list = list(nx.utils.pairwise(cycle))

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
    plt.title("The optimal path using Greedy Approach")
    plt.show()
    return edge_list
