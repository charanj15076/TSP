from geopy.distance import geodesic
import math
import networkx as nx
from approximation_techniques.christofides import christofides
from approximation_techniques.simulated_annealing import simulated_annealing
from approximation_techniques.greedy import greedy
#from networkx.algorithms.approximation.traveling_salesman import simulated_annealing_tsp

def solve_tsp(location,technique):
    #Convert location dictionary to pos dictionary
    city=0
    pos=dict()
    mapper_dict=dict()
    for i in location:
        pos[city]=location[i]
        mapper_dict[city]=i
        city+=1
    
    # Create a complete graph from the distance matrix
    G = nx.Graph()
    #pos[0] = (0.5, 0.5)
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
            dist = dist
            G.add_edge(i, j, weight=dist)

    if (technique=="Christofides"):
        tsp_solution = christofides(G,pos,mapper_dict,weight="weight")
    elif (technique=="Simulated Annealing"):
        tsp_solution = simulated_annealing(G,pos,mapper_dict,weight="weight",epochs=50,temperature=300)
    elif (technique=="Greedy"):
        tsp_solution = greedy(G,pos,mapper_dict,weight="weight")
    #Default
    else:
        tsp_solution = christofides(G,pos,mapper_dict,weight="weight")
    return tsp_solution

# Example locations with city names as keys and (latitude, longitude) as values
locations = {
    "City1": [52.5200, 13.4050],
    "City2": [53.5511, 9.9937],
    "City3": [48.1351, 11.5820],
    "City4": [50.9375, 6.9603],
    "City5": [50.1109, 8.6821]
}

#tsp_solution = solve_tsp(locations,"Christofides")
tsp_solution = solve_tsp(locations,"Simulated Annealing")
#tsp_solution = solve_tsp(locations,"Greedy")
print(tsp_solution)
