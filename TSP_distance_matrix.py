from geopy.distance import geodesic
import matplotlib.pyplot as plt
import math
import networkx as nx

def solve_tsp(pos):
    # Create a complete graph from the distance matrix
    G = nx.Graph()
    #pos[0] = (0.5, 0.5)
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
            dist = dist
            G.add_edge(i, j, weight=dist)
    # Solve TSP using Christofides algorithm
    tsp_solution = nx.algorithms.approximation.christofides(G, weight="weight")
    edge_list = list(nx.utils.pairwise(tsp_solution))

    # Draw closest edges on each node only
    nx.draw_networkx_edges(G, pos, edge_color="blue", width=0.5)

    # Draw the route
    nx.draw_networkx(
        G,
        pos,
        with_labels=True,
        edgelist=edge_list,
        edge_color="red",
        node_size=200,
        width=3,
    )
    plt.title("The optimal path using Cristofides")
    plt.show()
    return tsp_solution

# Example locations with city names as keys and (latitude, longitude) as values
locations = {
    0: [52.5200, 13.4050],
    1: [53.5511, 9.9937],
    2: [48.1351, 11.5820],
    3: [50.9375, 6.9603],
    4: [50.1109, 8.6821]
}

#distance_matrix = calculate_distance_matrix(locations)
#print(distance_matrix)

tsp_solution = solve_tsp(locations)
print(tsp_solution)
