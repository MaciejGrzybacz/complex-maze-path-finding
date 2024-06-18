#!/usr/bin/env python
"""
This module is the entry point for the application.
"""

from src.graph_utils import convert_grid_to_graph
from src.display_maze import Drawer
from networkx import read_gexf  # type: ignore


if __name__ == "__main__":
    ROWS = 10
    COLS = 10
    CELL_SIZE = 40
    ITERATIONS = 3

    maze = read_gexf("data/maze.gexf")
    graph = read_gexf("data/graph.gexf")
    # graph = convert_grid_to_graph(maze)

    drawer = Drawer(ROWS, COLS, CELL_SIZE)
    drawer.setup(maze)
    drawer.draw(
        ITERATIONS,
        file_path="data/aco_state.jsonl",
    )
