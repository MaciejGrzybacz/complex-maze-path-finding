"""
Module for displaying the path-finding process
of the ACO algorithm.

This module provides functions for displaying the maze together
with the ants exploring it trying to find the shortest path.
"""

import networkx as nx  # type: ignore
import pygame  # type: ignore
from pygame.color import THECOLORS as c
from time import sleep
from typing import List, Tuple, Dict

DEFAULT_BORDER_COLOR = c["black"]
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
        self.screen.fill(c["white"])

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
                pygame.draw.line(
                    self.screen, c["black"], (x1, y1), (x2, y2), 2
                )

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
        color: Tuple[int, int, int, int] = c["red"],
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
        color: Tuple[int, int, int, int] = c["blue"],
        dash: bool = False,
        draw_ends: bool = False,
    ):
        """
        Draw path through maze

        Args:
            path: list of vertices constituting a path
            color: color of path to draw
            dash: TODO
            draw_ends: TODO

        Returns:
            Nothing
        """
        # parameters
        line_width = int(self.cell_size / 6)
        box_start = int(self.cell_size / 12) - 1
        circle_size = line_width * 3 + 1

        # first point
        u = path[0]
        uy, ux = divmod(u, self.cols)

        # circle at start
        if draw_ends:
            pygame.draw.ellipse(
                self.screen,
                color,
                (
                    (
                        self.cell_size * (ux + 1 / 2) - circle_size / 2,
                        self.cell_size * (uy + 1 / 2) - circle_size / 2,
                    ),
                    (circle_size, circle_size),
                ),
            )

        for i in range(1, len(path)):
            v = path[i]

            # start and end position in graph
            vy, vx = divmod(v, self.cols)

            # start position in gui
            x1 = self.cell_size / 2 + ux * self.cell_size
            y1 = self.cell_size / 2 + uy * self.cell_size

            # end position in gui
            x2: float
            y2: float
            if dash:  # dashed line
                if vx == ux:
                    x2 = vx * self.cell_size + self.cell_size / 2
                    if vy > uy:
                        y2 = vy * self.cell_size
                    else:
                        y2 = vy * self.cell_size + self.cell_size
                else:
                    if vx > ux:
                        x2 = vx * self.cell_size
                    else:
                        x2 = vx * self.cell_size + self.cell_size
                    y2 = vy * self.cell_size + self.cell_size / 2
            else:  # normal line
                x2 = vx * self.cell_size + self.cell_size / 2
                y2 = vy * self.cell_size + self.cell_size / 2

            # draw line
            pygame.draw.line(
                self.screen, color, (x1, y1), (x2, y2), line_width
            )

            # rect for making line smooth
            pygame.draw.rect(
                self.screen,
                color,
                (
                    (x1 - box_start, y1 - box_start),
                    (line_width, line_width),
                ),
            )

            # make current vertex previous
            u = v
            uy, ux = divmod(u, self.cols)

        # circle at end
        if draw_ends:
            pygame.draw.ellipse(
                self.screen,
                color,
                (
                    (
                        self.cell_size * (vx + 1 / 2) - circle_size / 2,
                        self.cell_size * (vy + 1 / 2) - circle_size / 2,
                    ),
                    (
                        circle_size,
                        circle_size,
                    ),
                ),
            )

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
