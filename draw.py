#!/usr/bin/env python
"""
This module is the entry point for the application.
"""

from src.graph_utils import convert_grid_to_graph
from src.display_maze import Drawer
from networkx import from_edgelist  # type: ignore
from sys import argv
from os.path import isfile


if __name__ == "__main__":
    CELL_SIZE = 40
    ROWS = 10
    COLS = 10
    ITERATIONS = 3
    ANTS = 20

    if isfile("data/settings.txt"):
        with open("data/settings.txt", "r") as s:
            ROWS, COLS, ITERATIONS, ANTS = eval(s.read())

    with open("data/maze.txt", "r") as m:
        maze = from_edgelist(eval(m.read()))
    graph = convert_grid_to_graph(maze)

    if len(argv) > 1:
        drawer = Drawer(
            ROWS,
            COLS,
            CELL_SIZE,
            float(argv[1]),
        )
    else:
        drawer = Drawer(ROWS, COLS, CELL_SIZE)

    drawer.setup(maze)
    drawer.draw(
        ITERATIONS,
        file_path="data/aco_state.jsonl",
    )
