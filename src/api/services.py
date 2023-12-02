from data_collection import *
from fwa import FWAlgorithm

import osmnx


# Get all shortest paths from all locations in a centroid coordinate
# Input: center coordinates, list of blockage coordinates, distance
# Output: shortest distance & path matrices
def run_simulation(blockages_list, lat_center, lng_center, distance):
        
        G = generate_graph_from_centroid(lat_center, lng_center, distance)

	# build all-pairs shortest paths
	new_G = all_pairs_shortest_paths(G, locations)

	if (technique=="Christofides"):
                tsp_solution = christofides(new_G, mapper_dict,weight="weight")
        elif (technique=="Simulated Annealing"):
                tsp_solution = simulated_annealing(new_G,mapper_dict,weight="weight",epochs=50,temperature=300)
        elif (technique=="Greedy"):
        tsp_solution = greedy(new_G,mapper_dict,weight="weight")
    #Default
    else:
        tsp_solution = christofides(new_G,mapper_dict,weight="weight")
    return tsp_solution

