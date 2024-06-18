#!/usr/bin/env python
"""
This module is the entry point for the application.
"""

from src.path_finding import AntColonyOptimization
from src.evaluation import compare_with_dijkstra
from src.graph_generation import generate_maze
from src.graph_utils import convert_grid_to_graph, node_tuple_to_int
from networkx import to_edgelist  # type: ignore
from sys import argv


if __name__ == "__main__":
    CELL_SIZE = 40
    ROWS = 10
    COLS = 10
    ITERATIONS = 3

    if len(argv) > 1:
        ROWS = int(argv[1])
        COLS = int(argv[1])
    elif len(argv) > 2:
        ITERATIONS = int(argv[2])

    with open("data/settings.txt", "w") as s:
        s.write(str((ROWS, COLS, ITERATIONS)))

    maze = generate_maze(ROWS, COLS)
    with open("data/maze.txt", "w") as m:
        m.write(str(to_edgelist(maze)))
    graph = convert_grid_to_graph(maze)

    aco = AntColonyOptimization(
        graph,
        n_ants=100,
        n_best=3,
        n_iterations=ITERATIONS,
        filename="data/aco_state.jsonl",
        decay=0.5,
        alpha=1,
        beta=1,
    )

    upper_right_corner = node_tuple_to_int((0, COLS - 1), COLS)
    lower_left_corner = node_tuple_to_int((ROWS - 1, 0), COLS)
    aco_path, dijkstra_path = compare_with_dijkstra(
        graph, lower_left_corner, upper_right_corner, aco
    )
