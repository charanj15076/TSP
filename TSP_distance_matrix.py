#!/usr/bin/env python
# coding: utf-8

# In[3]:


from geopy.distance import geodesic

def calculate_distance_matrix(locations):
    distance_matrix = {}
    for source_city, source_coords in locations.items():
        distances = {}
        for target_city, target_coords in locations.items():
            if source_city != target_city:
                distance = geodesic(source_coords, target_coords).kilometers
                distances[target_city] = distance
        distance_matrix[source_city] = distances
    return distance_matrix

# Example locations with city names as keys and (latitude, longitude) as values
locations = {
    "City1": (52.5200, 13.4050),
    "City2": (53.5511, 9.9937),
    "City3": (48.1351, 11.5820),
    "City4": (50.9375, 6.9603),
    "City5": (50.1109, 8.6821),

}

distance_matrix = calculate_distance_matrix(locations)
distance_matrix


# In[4]:


import networkx as nx

def solve_tsp(distance_matrix):
    # Create a complete graph from the distance matrix
    G = nx.Graph()
    for city, distances in distance_matrix.items():
        for target_city, distance in distances.items():
            G.add_edge(city, target_city, weight=distance)

    # Solve TSP using Christofides algorithm
    tsp_solution = nx.approximation.traveling_salesman_problem(G, cycle=True)

    return tsp_solution

tsp_solution = solve_tsp(distance_matrix)
tsp_solution


# In[ ]:




