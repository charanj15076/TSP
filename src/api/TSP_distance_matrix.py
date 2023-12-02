#from geopy.distance import geodesic
import math
import networkx as nx
import osmnx as ox
from approximation_techniques.christofides import christofides
from approximation_techniques.simulated_annealing import simulated_annealing
from approximation_techniques.greedy import greedy
#from networkx.algorithms.approximation.traveling_salesman import simulated_annealing_tsp

def solve_tsp(location,technique):
    """
    #Convert location dictionary to pos dictionary
    city=0
    pos=dict()
    mapper_dict=dict()
    for i in location:
        pos[city]=location[i]
        mapper_dict[city]=i
        city+=1
    """
    locations=list(location.values())
    latitudes=[loc[0] for loc in locations]
    longitudes=[loc[1] for loc in locations]
    #print(latitudes)
    #print(longitudes)
    lookup=dict()
    # Create a complete graph from the distance matrix
    """
    G1 = nx.Graph()
    #pos[0] = (0.5, 0.5)
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
            dist = dist
            G1.add_edge(i, j, weight=dist)
    """
    
    north = max(latitudes) * 1.0001
    south = min(latitudes) * 1.0001
    west = min(longitudes) * 1.0001
    east = max(longitudes) * 1.0001
    
    # Download the street network graph for the specified area
    G1 = ox.graph_from_bbox(north, south, east, west, retain_all=True, truncate_by_edge=True, network_type='drive')
    #G1 = ox.graph_from_point((33.72773047528036, -117.95608520507814), dist=80, network_type='walk')
    print(G1)
    G = nx.Graph()
    cordinates=list(location.values())
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

    """
    G1 = ox.graph_from_point((33.72773047528036, -117.95608520507814), dist=80, network_type='walk')
    source=ox.distance.nearest_nodes(G1,-117.96016216278078,33.725303380272706, return_dist=False)
    destination=ox.distance.nearest_nodes(G1,-117.95501232147217,33.72291191070952, return_dist=False)
    #print(source)
    shortest_path_length=nx.shortest_path_length(G1,source,destination)
    print(type(shortest_path_length))
    shortest_paths=nx.shortest_path(G1,source,destination)
    print(shortest_paths)
    #path=dict(nx.all_pairs_shortest_path(G1))
    #print(G1)
    #print(path)
    #G=nx.Graph(G1)
    """
    
    if (technique=="Christofides"):
        tsp_solution = christofides(G,weight="weight")
    elif (technique=="Simulated Annealing"):
        tsp_solution = simulated_annealing(G,weight="weight",epochs=50,temperature=300)
    elif (technique=="Greedy"):
        tsp_solution = greedy(G,weight="weight")
    #Default
    else:
        tsp_solution = christofides(G,weight="weight")
    return tsp_solution,lookup

    
# Example locations with city names as keys and (latitude, longitude) as values
#latitude, longtiude
locations = {
    "City1": [33.725303380272706, -117.96016216278078],
    "City2": [33.72291191070952, -117.95501232147217],
    "City3": [33.728658464055954, -117.96136379241945],
    "City4": [33.72773047528036,  -117.95608520507814],
}
#locations=list(locations1.values())
#print(locations)

tsp_solution, lookup = solve_tsp(locations,"Christofides")
#print(tsp_solution)
#print(lookup)
#tsp_solution, lookup = solve_tsp(locations,"Simulated Annealing")
#print(tsp_solution)
#print(lookup)
# tsp_solution, lookup = solve_tsp(locations,"Greedy")
#solve_tsp(locations,"Greedy")
print(tsp_solution)
print(lookup)
print("Hello")

