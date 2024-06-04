"""
This module is the entry point for the application.
"""

from src.path_finding import AntColonyOptimization
from src.evaluation import compare_with_dijkstra
from src.graph_generation import generate_maze
from src.graph_utils import convert_grid_to_graph, node_tuple_to_int
from src.display_maze import Drawer, c

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
    ROWS = 12
    COLS = 12
    CELL_SIZE = 40

    maze = generate_maze(ROWS, COLS)
    graph = convert_grid_to_graph(maze)

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

    aco_path, dijkstra_path = compare_with_dijkstra(
        graph, lower_left_corner, upper_right_corner, aco
    )

    drawer = Drawer(ROWS, COLS, CELL_SIZE)
    drawer.setup()
    drawer.draw_maze(maze)
    drawer.draw_path(aco_path, c["blue"], draw_ends=True)
    drawer.draw_path(dijkstra_path, c["red"], True)
    drawer.display_loop()
