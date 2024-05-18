"""
Unit tests for graph_generation module.
"""

import networkx as nx

from src.graph_generation import generate_maze_kruskal, generate_random_graph


# generate_maze_kruskal tests
def test_connectivity():
    """Tests if the maze is a connected graph."""
    maze = generate_maze_kruskal(5, 5)
    assert nx.is_connected(maze)

def test_no_cycles():
    """Tests if the maze has no cycles."""
    maze = generate_maze_kruskal(10, 9)
    assert nx.is_tree(maze)

def test_dimensions():
    """Tests if the maze has a correct number of nodes and edges."""
    rows, cols = 10, 14
    maze = generate_maze_kruskal(rows, cols)
    assert maze.number_of_nodes() == rows * cols


# generate_random_graph tests
def test_number_of_nodes():
    """Tests if the generated graph has the correct number of nodes."""
    n = 15
    graph = generate_random_graph(n, 0.5)
    assert graph.number_of_nodes() == n

def test_edge_weights():
    """Tests if the edge weights are within the specified range."""
    min_weight = 5
    max_weight = 20
    graph = generate_random_graph(10, 0.5, min_weight=min_weight,
                                  max_weight=max_weight)
    for _, _, w in graph.edges(data=True):
        assert min_weight <= w["weight"] <= max_weight
