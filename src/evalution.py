"""
This module contains functions for evaluating the performance
of ACO when compared to the other shortest-path finding
algorithms.
"""

import networkx as nx
import time
from .path_finding import AntColonyOptimization

def compare_with_dijkstra(graph: nx.Graph,
                          start: int,
                          end: int,
                          aco: AntColonyOptimization):
    
    # Compute the shortest path using Dijkstra's algorithm
    dij_start = time.time()
    dijkstra_path = nx.dijkstra_path(graph, start, end)
    dij_end = time.time()
    dijkstra_length = len(dijkstra_path) - 1
    
    # Compute the shortest path using ACO
    aco_start = time.time()
    aco_path, aco_length = aco.run(start, end)
    aco_end = time.time()
    
    print(f"Dijkstra's shortest path: {dijkstra_path}")
    print(f"Dijkstra's path length: {dijkstra_length}")
    print(f"Dijkstra's running time: {dij_end - dij_start:.2f}")
    print(f"ACO shortest path: {aco_path}")
    print(f"ACO path length: {aco_length}")
    print(f"ACO running time: {aco_end - aco_start:2f}")
    
    if aco_length == dijkstra_length:
        print("ACO has found the optimal path.")
    else:
        print("ACO did not find the optimal path.")
