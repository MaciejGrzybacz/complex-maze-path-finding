"""
Module for generating random graphs with weighted edges.

This module provides functions for creating NetworkX graphs with
random structure and edge weights.
"""

import networkx as nx  # type: ignore
import numpy as np
import random
from typing import Optional


# Number of edges added to the graph during maze
# generation to create cycles
NEW_EDGES_FRAC = 0.015


def generate_random_graph(
    n: int,
    edge_p: float,
    seed: int = 42,
    min_weight: int = 1,
    max_weight: int = 10,
) -> nx.Graph:
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


def _generate_maze_kruskal(rows: int, cols: int) -> nx.Graph:
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
    edges_with_weights = [
        (u, v, {"weight": np.random.random_sample()}) for u, v in edges
    ]

    mod_graph = nx.Graph()
    mod_graph.add_edges_from(edges_with_weights)

    mst = nx.minimum_spanning_tree(mod_graph, algorithm="kruskal")

    for _, _, d in mst.edges(data=True):
        del d["weight"]

    return mst


def generate_maze(rows: int, cols: int, extra_edges: Optional[int] = None):
    """
    Generate a random maze. At least one cycle in the maze is guaranteed.

    Functionality note:
    Proportion of extra_edges with respect to
    the total number of possible edges to add should not be high and
    should certainly be less than 50%.

    Args:
        rows: Number of rows in the maze
        cols: Number of columns in the maze
        extra_edges: Number of extra edges added to try to create a cycle

    Returns:
        Maze represented as a connected NetworkX graph with a cycle.
    """
    if extra_edges is None:
        # Approximate number of edges that can be added multiplied
        # by the fraction that we want to add
        edge_num = rows * cols * 4
        extra_edges = int(NEW_EDGES_FRAC * edge_num)

    graph = _generate_maze_kruskal(rows, cols)

    def get_valid_neighbors(node: tuple[int, int], rows: int, cols: int):
        """
        Get all valid nodes with which the given node can be connected.
        """
        row, col = node
        neighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ]
        return [
            (r, c) for r, c in neighbors if 0 <= r < rows and 0 <= c < cols
        ]

    # Add extra edges to create cycles
    # Iterate for a number of extra edges. If the extra edges do not yield
    # a cycle then iterate until we get a first cycle.
    added_edges = 0
    while added_edges < extra_edges or nx.is_tree(graph):
        u = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        valid_neighbors = get_valid_neighbors(u, rows, cols)

        if valid_neighbors:
            v = random.choice(valid_neighbors)
            if not graph.has_edge(u, v):
                graph.add_edge(u, v)
                added_edges += 1

    return graph
