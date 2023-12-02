import math
import networkx as nx
import osmnx as ox
from approximation_techniques.christofides import christofides
from approximation_techniques.simulated_annealing import simulated_annealing
from approximation_techniques.greedy import greedy

def solve_tsp(location,technique):
    latitudes=[loc[0] for loc in location]
    longitudes=[loc[1] for loc in location]

    lookup=dict()

    # Create a complete graph from the distance matrix    
    north = max(latitudes)
    south = min(latitudes)
    west = min(longitudes)
    east = max(longitudes)

    north = north + abs(north * 0.000025)
    south = south - abs(south * 0.000025)
    west = west - abs(west * 0.000025)
    east = east + abs(east * 0.000025)

    # Download the street network graph for the specified area
    G1 = ox.graph_from_bbox(north, south, east, west, retain_all=True, truncate_by_edge=True, network_type='drive')
    print(G1)
    G = nx.Graph()

    cordinates=list(location)
    for i in range(len(cordinates)):
        for j in range(len(cordinates)):
            if i==j:
                continue
            source=ox.distance.nearest_nodes(G1,cordinates[i][1],cordinates[i][0], return_dist=False)
            destination=ox.distance.nearest_nodes(G1,cordinates[j][1],cordinates[j][0], return_dist=False)
            shortest_path_length=nx.shortest_path_length(G1,source,destination)
            shortest_paths=nx.shortest_path(G1,source,destination)
            G.add_edge(source, destination, weight=shortest_path_length,)
            lookup[(source,destination)]=shortest_paths

    if (technique=="Christofides"):
        tsp_solution = christofides(G,weight="weight")
    elif (technique=="Simulated Annealing"):
        tsp_solution = simulated_annealing(G,weight="weight",epochs=50,temperature=300)
    elif (technique=="Greedy"):
        tsp_solution = greedy(G,weight="weight")
    else:
        tsp_solution = christofides(G,weight="weight")


    # build edge list
    edge_list = []
    for edge in tsp_solution:
        gdf_edge = ox.utils_graph.route_to_gdf(G1, lookup[edge], weight='length')
        edge_list.append(gdf_edge)

    return edge_list