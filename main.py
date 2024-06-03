"""
This module is the entry point for the application.
"""

from src.path_finding import AntColonyOptimization
from src.evaluation import compare_with_dijkstra
from src.graph_generation import generate_maze
from src.graph_utils import convert_grid_to_graph, node_tuple_to_int

import networkx as nx  # type: ignore


def ensure_undirected_with_symmetry(graph: nx.Graph) -> nx.Graph:
    """
    Converts a graph to an undirected graph and ensures that both directions
    of each edge are explicitly included.

    Parameters:
        graph: The graph to be converted.

    Returns:
        The undirected graph with symmetric edges.
    """
    undirected_graph = nx.Graph()
    undirected_graph.add_nodes_from(graph.nodes())

    for u, v in graph.edges():
        undirected_graph.add_edge(u, v)
        undirected_graph.add_edge(v, u)

    return undirected_graph


if __name__ == "__main__":
    ROWS = 10
    COLS = 10
    graph = generate_maze(ROWS, COLS)
    graph = convert_grid_to_graph(graph)

    aco = AntColonyOptimization(
        graph,
        n_ants=10,
        n_best=3,
        n_iterations=10,
        decay=0.5,
        alpha=1,
        beta=1,
    )

    upper_right_corner = node_tuple_to_int((0, COLS - 1), COLS)
    lower_left_corner = node_tuple_to_int((ROWS - 1, 0), COLS)

    compare_with_dijkstra(graph, lower_left_corner, upper_right_corner, aco)
