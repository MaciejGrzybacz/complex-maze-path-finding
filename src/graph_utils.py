"""
This module contains functions for converting between different graph
representations. For example it has functions for converting nodes of
a graph representedas tuples to integers and the same in the other
direction.

The main usage of this module is to prepare graphs to serve as
input to the ACO algorithm.
"""

import networkx as nx  # type: ignore
from typing import Tuple


def node_tuple_to_int(node: Tuple[int, int], grid_width: int) -> int:
    """
    Converts a grid node represented as a tuple (row, col) to an integer.

    Parameters:
        node: A tuple (row, col) representing the node in the grid.
        grid_width: The width of the grid.

    Returns:
        An integer representing the node.
    """
    row, col = node
    return row * grid_width + col


def node_int_to_tuple(node: int, grid_width: int) -> Tuple[int, int]:
    """
    Converts an integer node representation to a tuple (row, col).

    Parameters:
        node: An integer representing the node.
        grid_width: The width of the grid.

    Returns:
        A tuple (row, col) representing the node in the grid.
    """
    row = node // grid_width
    col = node % grid_width
    return row, col


def convert_grid_to_graph(grid_graph: nx.Graph) -> nx.Graph:
    """
    Converts a grid with nodes represented as tuples (row, col)
    to a NetworkX graph where nodes are represented by integers.

    Parameters:
        grid_graph: A NetworkX graph where nodes are tuples (row, col).

    Returns:
        A NetworkX graph with nodes represented as integers.
    """
    undirected_graph = nx.Graph()
    grid_width = max(node[1] for node in grid_graph.nodes()) + 1

    for node in grid_graph.nodes():
        int_node = node_tuple_to_int(node, grid_width)
        undirected_graph.add_node(int_node)

    for u, v in grid_graph.edges():
        int_u = node_tuple_to_int(u, grid_width)
        int_v = node_tuple_to_int(v, grid_width)
        undirected_graph.add_edge(int_u, int_v)

    return undirected_graph
