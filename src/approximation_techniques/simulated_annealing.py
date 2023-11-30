import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.traveling_salesman import simulated_annealing_tsp

def simulated_annealing(G,pos,mapper_dict,weight="weight"):
    nodes=simulated_annealing_tsp(G,"greedy",weight="weight")
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
    plt.title("The optimal path using Simulated Annealing")
    plt.show()

    return edge_list

def simulated_annealing_tsproblem(G,pos,mapper,weight="weight"):
    init_cycle="greedy"
    source=None
    temp=1000
    move="1-1"
    epochs=30
    N_inner=100
    alpha=0.01
    seed=None

    cycle = greedy_tsp(G, weight=weight, source=source)
    if G.number_of_nodes() == 2:
        return cycle

    # Find the cost of initial solution
    cost = sum(G[u][v].get(weight, 1) for u, v in pairwise(cycle))

    move = swap_two_nodes
    count = 0
    best_cycle = cycle.copy()
    best_cost = cost
    while count <= epochs and temp > 0:
        count += 1
        for i in range(N_inner):
            adj_sol = move(cycle, seed)
            adj_cost = sum(G[u][v].get(weight, 1) for u, v in pairwise(adj_sol))
            delta = adj_cost - cost
            if delta <= 0:
                # Set current solution the adjacent solution.
                cycle = adj_sol
                cost = adj_cost

                if cost < best_cost:
                    count = 0
                    best_cycle = cycle.copy()
                    best_cost = cost
            else:
                # Accept even a worse solution with probability p.
                p = math.exp(-delta / temp)
                if p >= seed.random():
                    cycle = adj_sol
                    cost = adj_cost
        temp -= temp * alpha

    return best_cycle

def greedy_tsp(G,weight="weight",source=None):
    source=None
    N = len(G) - 1
    # This check ignores selfloops which is what we want here.
    if any(len(nbrdict) - (n in nbrdict) != N for n, nbrdict in G.adj.items()):
        raise nx.NetworkXError("G must be a complete graph.")

    if source is None:
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
    return cycle

def swap_two_nodes(soln,seed):
    a, b = seed.sample(range(1, len(soln) - 1), k=2)
    soln[a], soln[b] = soln[b], soln[a]
    return soln
