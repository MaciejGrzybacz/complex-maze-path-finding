"""
Module for displaying the path-finding process
of the ACO algorithm.

This module provides functions for displaying the maze together
with the ants exploring it trying to find the shortest path.
"""

import networkx as nx  # type: ignore
import pygame  # type: ignore
from time import sleep
from typing import List, Tuple, Dict

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DEFAULT_BORDER_COLOR = BLACK
DEFAULT_SLEEP_TIME = 0.02


class Drawer:
    """
    Class for drawing mazes and paths.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        cell_size: int = 20,
        sleep_time: float = DEFAULT_SLEEP_TIME,
    ):
        """
        Initialize maze drawer with some parameters
        """

        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols
        self.width, self.height = cols * cell_size, rows * cell_size
        self.sleep_time = sleep_time

    def setup(self):
        """
        Setup, pygame init

        Args:
            Nothing

        Returns:
            Nothing
        """

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze")
        self.screen.fill(WHITE)

    def draw_maze(
        self,
        maze: nx.Graph,
    ):
        """
        Display maze given by a graph.

        Works by comparing graph to full 2d grid and drawing walls where
        there is no edge. Also draws red border with entrance and exit
        around maze.

        Args:
            mst: graph
            rows: amount rows in maze
            cols: amount columns in maze
            cell_size: size of cell to draw

        Returns:
            Nothing
        """

        full = nx.grid_2d_graph(self.rows, self.cols)
        edges = maze.edges()

        for u, v in full.edges():
            if (u, v) not in edges:
                if u[0] == v[0]:  # horizontal
                    x1 = (
                        u[1] + v[1]
                    ) * self.cell_size / 2 + self.cell_size / 2
                    x2 = x1
                    y1 = (
                        u[0] + v[0] - 1
                    ) * self.cell_size / 2 + self.cell_size / 2
                    y2 = y1 + self.cell_size

                else:  # vertical
                    x1 = (
                        u[1] + v[1] - 1
                    ) * self.cell_size / 2 + self.cell_size / 2
                    x2 = x1 + self.cell_size
                    y1 = (
                        u[0] + v[0]
                    ) * self.cell_size / 2 + self.cell_size / 2
                    y2 = y1

                # draw wall
                pygame.draw.line(self.screen, BLACK, (x1, y1), (x2, y2), 2)

        # border
        border_width = int(self.cell_size / 10)
        pygame.draw.line(
            self.screen,
            DEFAULT_BORDER_COLOR,
            (0, self.cell_size),
            (0, self.height),
            border_width,
        )
        pygame.draw.line(
            self.screen,
            DEFAULT_BORDER_COLOR,
            (0, 0),
            (self.width, 0),
            border_width,
        )
        pygame.draw.line(
            self.screen,
            DEFAULT_BORDER_COLOR,
            (0, self.height - 1),
            (self.width, self.height - 1),
            border_width,
        )
        pygame.draw.line(
            self.screen,
            DEFAULT_BORDER_COLOR,
            (self.width - 1, 0),
            (self.width - 1, self.height - self.cell_size),
            border_width,
        )

        # update
        pygame.display.flip()

    def draw_pheromone(
        self,
        pheromone: Dict[Tuple[int, int], float],
        color: Tuple[int, int, int] = RED,
    ):
        """
        Draw pheromone levels in maze

        Args:
            pheromone: level of pheromone on visited edges
            color: color of path to draw

        Returns:
            Nothing
        """
        pass  # TODO

    def draw_path(
        self,
        path: List[int],
        color: Tuple[int, int, int] = BLUE,
    ):
        """
        Draw path through maze

        Args:
            path: list of vertices constituting a path
            color: color of path to draw

        Returns:
            Nothing
        """
        u = path[0]
        line_width = int(self.cell_size / 6)
        box_start = int(self.cell_size / 12) - 1

        for i in range(1, len(path)):
            v = path[i]

            # start and end of line
            vy, vx = divmod(v, self.cols)
            uy, ux = divmod(u, self.cols)
            x1 = self.cell_size / 2 + ux * self.cell_size
            y1 = self.cell_size / 2 + uy * self.cell_size
            x2 = self.cell_size / 2 + vx * self.cell_size
            y2 = self.cell_size / 2 + vy * self.cell_size

            # line
            pygame.draw.line(
                self.screen, color, (x1, y1), (x2, y2), line_width
            )

            # rect for making line smooth
            pygame.draw.rect(
                self.screen,
                color,
                ((x1 - box_start, y1 - box_start), (line_width, line_width)),
            )
            u = v

        # same square as before
        pygame.display.flip()

    def display_loop(self):
        """
        Simple event loop for displaying graphics, quits when window is closed

        Args:
            Nothing

        Returns:
            Nothing
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            sleep(self.sleep_time)

        pygame.quit()
