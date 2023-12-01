import networkx as nx
import osmnx as ox
from itertools import islice

# this returns a network graph of paths where the source is in the center
def generate_graph_from_centroid(source_latitude, source_longtitude, distance_meter):
    source_point = source_latitude, source_longtitude

    # Download the street network graph for the specified area
    graph = ox.graph_from_point(source_point, dist=distance_meter, network_type='all')

    return graph


# this returns nodes & edges as geodataframes from a graph
def convert_to_gdf(graph):
    # paths = dict(nx.all_pairs_shortest_path(graph))

    gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)

    return gdf_nodes, gdf_edges


# this is the distance matrix used by fwa
def get_input_distance_matrix(graph, source_latitude, source_longtitude):
    source_point = source_latitude, source_longtitude
    source_node = ox.distance.nearest_nodes(graph, source_point[1], source_point[0])
    all_nodes = [v for v, d in graph.out_degree()]
    
    all_paths = []
    for target_node in all_nodes:
        paths = list(nx.all_simple_paths(graph, source=source_node, target=target_node, cutoff=20))
        all_paths.extend(paths)

    # Fill in the distance matrix with actual distances between nodes
    distance_matrix = {}
    for path in all_paths:
        for i in range(len(path) - 1):
            node1, node2 = path[i], path[i + 1]

            edge_data = graph.get_edge_data(node1, node2, 0)
            if edge_data:
                distance = edge_data['length']  
                distance_matrix[node1,node2] = distance

    return distance_matrix

    
