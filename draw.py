#!/usr/bin/env python
"""
This module is the entry point for the application.
"""

from src.graph_utils import convert_grid_to_graph
from src.display_maze import Drawer
from networkx import from_edgelist  # type: ignore


if __name__ == "__main__":
    ROWS = 10
    COLS = 10
    CELL_SIZE = 40
    ITERATIONS = 3

    with open("data/maze.txt", "r") as m:
        maze = from_edgelist(eval(m.read()))
    graph = convert_grid_to_graph(maze)

    drawer = Drawer(ROWS, COLS, CELL_SIZE)
    drawer.setup(maze)
    drawer.draw(
        ITERATIONS,
        file_path="data/aco_state.jsonl",
    )
