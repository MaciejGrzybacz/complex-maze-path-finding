"""
Unit tests for graph_generation module.
"""

import networkx as nx

from src.graph_generation import _generate_maze_kruskal, generate_random_graph
from src.graph_generation import generate_maze

# _generate_maze_kruskal tests
def test_kruskal_connectivity():
    """Tests if the maze is a connected graph."""
    maze = _generate_maze_kruskal(5, 5)
    assert nx.is_connected(maze)

def test_kruskal_no_cycles():
    """Tests if the maze has no cycles."""
    maze = _generate_maze_kruskal(10, 9)
    assert nx.is_tree(maze)

def test_kruskal_dimensions():
    """Tests if the maze has a correct number of nodes and edges"""
    rows, cols = 10, 14
    maze = _generate_maze_kruskal(rows, cols)
    assert maze.number_of_nodes() == rows * cols
    assert maze.number_of_edges() == maze.number_of_nodes() - 1


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


# generate_maze tests
def test_maze_connectivity():
    """Tests if the graph is a connected graph."""
    maze = generate_maze(10, 10)
    assert nx.is_connected(maze)

def test_maze_has_cycles():
    """Tests if the graph contains cycles."""
    maze = generate_maze(20, 20)
    assert not nx.is_tree(maze)

def test_maze_dimensions():
    """Tests if the graph has a correct number of nodes."""
    rows, cols = 6, 8
    extra = 5
    maze = generate_maze(rows, cols, extra_edges=extra)
    assert maze.number_of_nodes() == rows * cols


def test_maze_auto_edge_calculation():
    """
    Tests if the default value for the number of extra edges
    gives us a maze with cycles.
    """
    rows, cols = 15, 20
    maze = generate_maze(rows, cols)
    assert not nx.is_tree(maze)
