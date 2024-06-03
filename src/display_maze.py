"""
Module for displaying the path-finding process
of the ACO algorithm.

This module provides functions for displaying the maze together
with the ants exploring it trying to find the shortest path.
"""

import networkx as nx  # type: ignore
import pygame  # type: ignore
from time import sleep


def draw_maze(
    mst: nx.Graph,
    rows: int,
    cols: int,
    cell_size: int = 20,
):
    """
    Display maze given by a graph.

    Works by comparing graph to full 2d grid and drawing walls where there is
    no edge. Also draws red border with entrance and exit around maze.

    Args:
        mst: graph
        rows: amount rows in maze
        cols: amount columns in maze
        cell_size: size of cell to draw

    Returns:
        Nothing

    """

    pygame.init()
    width, height = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze")
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill(white)
    full = nx.grid_2d_graph(rows, cols)
    mst_edges = mst.edges()

    for u, v in full.edges():
        if (u, v) not in mst_edges:
            if u[0] == v[0]:
                x1 = (u[1] + v[1]) * cell_size / 2 + cell_size / 2
                x2 = x1
                y1 = (u[0] + v[0] - 1) * cell_size / 2 + cell_size / 2
                y2 = y1 + cell_size

            else:
                x1 = (u[1] + v[1] - 1) * cell_size / 2 + cell_size / 2
                x2 = x1 + cell_size
                y1 = (u[0] + v[0]) * cell_size / 2 + cell_size / 2
                y2 = y1

            pygame.draw.line(screen, black, (x1, y1), (x2, y2), 2)

    pygame.draw.line(screen, (255, 0, 0), (0, cell_size), (0, height), 3)
    pygame.draw.line(screen, (255, 0, 0), (0, 0), (width, 0), 3)
    pygame.draw.line(
        screen, (255, 0, 0), (0, height - 1), (width, height - 1), 3
    )
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (width - 1, 0),
        (width - 1, height - cell_size),
        3,
    )

    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sleep(0.01)

    pygame.quit()
