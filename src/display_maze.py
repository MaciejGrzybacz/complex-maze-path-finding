"""
Module for displaying the path-finding process
of the ACO algorithm.

This module provides functions for displaying the maze together
with the ants exploring it trying to find the shortest path.
"""

import networkx as nx  # type: ignore
import pygame  # type: ignore
from collections import Counter
from pygame.color import THECOLORS as c
from time import sleep
from typing import List, Tuple, Dict
from math import exp

from src.state_loader import (
    load_state_by_iteration,
    DEFAULT_FILE_PATH,
)

Color = Tuple[int, int, int, int]


DEFAULT_BORDER_COLOR = c["black"]
DEFAULT_SLEEP_TIME = 0.5


class Drawer:
    """
    Class for drawing mazes and paths.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        cell_size: int = 20,
        t_delta: float = DEFAULT_SLEEP_TIME,
    ):
        """
        Initialize maze drawer with some parameters
        """

        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols
        self.width, self.height = cols * cell_size, rows * cell_size
        self.t_delta = t_delta

    def setup(self, maze):
        """
        Setup, pygame init

        Args:
            Nothing

        Returns:
            Nothing
        """

        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.font = pygame.font.SysFont("Comic Sans MS", 16)

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.ant_image = pygame.image.load("antcolony.png")
        self.ant_image = pygame.transform.scale(
            self.ant_image, (self.cell_size / 2, self.cell_size / 2)
        )

        pygame.display.set_caption("Maze")
        self.screen.fill(c["white"])

        self.edges = maze.edges()
        self.maze = pygame.surface.Surface((self.width, self.height))
        self._draw_maze(maze)

        self.ant_surface = pygame.surface.Surface(
            (self.width, self.height), pygame.SRCALPHA, 32
        )
        self.ant_surface.convert_alpha()

    def draw_maze(self):
        self.screen.blit(self.maze, (0, 0))

    def _draw_maze(
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

        self.maze.fill(c["white"])
        full = nx.grid_2d_graph(self.rows, self.cols)

        for u, v in full.edges():
            if (u, v) not in self.edges:
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
                pygame.draw.line(self.maze, c["black"], (x1, y1), (x2, y2), 2)

        # border
        border_width = int(self.cell_size / 10)
        pygame.draw.line(
            self.maze,
            DEFAULT_BORDER_COLOR,
            (0, 0),
            (0, self.height - self.cell_size),
            border_width,
        )
        pygame.draw.line(
            self.maze,
            DEFAULT_BORDER_COLOR,
            (0, 0),
            (self.width, 0),
            border_width,
        )
        pygame.draw.line(
            self.maze,
            DEFAULT_BORDER_COLOR,
            (0, self.height - 1),
            (self.width, self.height - 1),
            border_width,
        )
        pygame.draw.line(
            self.maze,
            DEFAULT_BORDER_COLOR,
            (self.width - 1, self.cell_size),
            (self.width - 1, self.height),
            border_width,
        )

        # update
        pygame.display.flip()

    def draw_pheromone(
        self,
        pheromone: Dict[Tuple[int, int], float],
        color: Color = c["red"],
    ):
        """
        Draw pheromone levels in maze

        Args:
            pheromone: level of pheromone on visited edges
            color: color of path to draw

        Returns:
            Nothing
        """
        for k, v in pheromone.items():
            uy, ux = divmod(k[0], self.cols)
            vy, vx = divmod(k[1], self.cols)
            intensity = 1 / (1 + exp(4 * (v - 1)))

            pygame.draw.line(
                self.maze,
                (
                    int(255 * intensity),
                    0,
                    0,
                ),
                (
                    ux * self.cell_size + self.cell_size / 2,
                    uy * self.cell_size + self.cell_size / 2,
                ),
                (
                    vx * self.cell_size + self.cell_size / 2,
                    vy * self.cell_size + self.cell_size / 2,
                ),
                int(self.cell_size / 8),
            )

    def draw_path(
        self,
        path: List[int],
        color: Color = c["blue"],
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

    def draw_ants(
        self,
        paths: List[List[int]],
        iter: int,
        color: Color = c["black"],
    ):
        """
        Draw ants going through maze in one iteration

        Args:
            paths: paths of ants
            iter: number of current iteration
            color: ant color

        Returns:
            Nothing
        """

        ant_size = self.cell_size / 4
        ants = [path[iter] for path in paths if len(path) > iter]
        ant_counts = Counter(ants)

        for ant, cnt in ant_counts.items():
            uy, ux = divmod(ant, self.cols)
            self._draw_ant_count(cnt, ux, uy)
            self._draw_ant(ant_size, color, ux, uy)

    def _draw_ant(
        self,
        ant_size: float,
        color: Color,
        ux: int,
        uy: int,
        dot: bool = True,
    ):
        if dot:
            self.screen.blit(
                self.ant_image, (ux * self.cell_size, uy * self.cell_size)
            )
            return

        pygame.draw.ellipse(
            self.screen,
            color,
            (
                (
                    self.cell_size * (ux + 1 / 2) - ant_size / 2,
                    self.cell_size * (uy + 1 / 2) - ant_size / 2,
                ),
                (ant_size, ant_size),
            ),
        )

    def _draw_ant_count(
        self,
        cnt: int,
        ux: int,
        uy: int,
    ):
        x = self.cell_size / 2 + ux * self.cell_size
        y = self.cell_size / 2 + uy * self.cell_size
        text_surface = self.font.render(f"{cnt}", False, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))

    def draw(
        self,
        iterations: int,
        file_path: str = DEFAULT_FILE_PATH,
    ):
        """
        Simple event loop for displaying graphics, quits when window is closed

        Args:
            Nothing

        Returns:
            Nothing
        """

        end = False

        for i in range(iterations):
            state = load_state_by_iteration(file_path, i)

            paths = state["all_paths"]
            paths = [path["path"] for path in paths]
            longest = max(len(path) for path in paths)

            pheromone = state["pheromone"]
            pheromones = {
                tuple(map(int, k.split("-"))): v for k, v in pheromone.items()
            }

            for i in range(longest):
                self.draw_maze()
                self.draw_pheromone(pheromones)
                self.draw_ants(paths, i)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = True
                        break

                if end:
                    break
                sleep(self.t_delta)

            if end:
                break

        pygame.quit()
