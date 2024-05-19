"""
Module for generating random graphs with weighted edges.

This module provides functions for creating NetworkX graphs with
random structure and edge weights.
"""

import networkx as nx
import numpy as np


def generate_random_graph(n: int, edge_p: float,
                          seed: int = 42,
                          min_weight: int = 1,
                          max_weight: int = 10) -> nx.Graph:
    """
    Generates a random graph with weighted edges.

    Args:
        n: Number of nodes.
        edge_p: Probability for edge creation.
        seed: Seed for random number generation (for reproducibility).
        min_weight: Minimum edge weight.
        max_weight: Maximum edge weight.

    Returns:
        The generated NetworkX graph.
    """
    graph = nx.gnp_random_graph(n=n, p=edge_p, seed=seed)

    for _, _, w in graph.edges(data=True):
        w["weight"] = np.random.randint(min_weight, max_weight + 1)

    return graph


def generate_maze_kruskal(rows: int, cols: int) -> nx.Graph:
    """
    Generates a random maze using Kruskal's algorithm.
    
    Args:
        rows: Number of rows in the maze
        cols: Number of columns in the maze
        
        Returns:
            Maze represented as a connected NetworkX graph.
    """
    graph = nx.grid_2d_graph(rows, cols)

    # Randomize the weight of the edges to prepare
    # for Kruskal's algorithm
    edges = list(graph.edges())
    np.random.shuffle(edges)
    # Floating-point weights between [0, 1) are used to randomize
    # the creation of the MST
    edges_with_weights = [(u, v, {"weight": np.random.random_sample()})
                          for u, v in edges]

    mod_graph = nx.Graph()
    mod_graph.add_edges_from(edges_with_weights)

    mst = nx.minimum_spanning_tree(mod_graph, algorithm="kruskal")

    for _, _, d in mst.edges(data=True):
        del d["weight"]

    return mst
