"""
This module implements various strategies that
can be used by Ant Colony Optimization algorithm
to find the shortest-paths in a graph.
"""

# mypy: no_implicit_optional = False

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Set
import networkx as nx  # type: ignore
import numpy as np


class MoveSelectionStrategy(ABC):
    """
    This strategy defines how an ant selects its next move
    based on the current pheromone levels and a heuristic.
    """

    @abstractmethod
    def select_move(
        self,
        graph: nx.Graph,
        pheromone: Dict[Tuple[int, int], float],
        explored: Set[int],
        current_node: int,
        alpha: float,
        beta: float,
    ) -> int:
        pass


class PheromoneUpdateStrategy(ABC):
    """
    This strategy defines how the pheromone levels are updated
    based on the paths found by the ants.
    """

    @abstractmethod
    def update_pheromone(
        self,
        pheromone: Dict[Tuple[int, int], float],
        paths: List[Tuple[List[int], int]],
        decay: float,
        n_best: int,
    ) -> Dict[Tuple[int, int], float]:
        pass


class PheromoneBasedMoveSelection(MoveSelectionStrategy):
    def select_move(
        self,
        graph: nx.Graph,
        pheromone: Dict[Tuple[int, int], float],
        explored: Set[int],
        current_node: int,
        alpha: float,
        beta: float,
    ) -> int:
        """
        Select the next move for an ant based on pheromone
        levels and heuristic information.

        Parameters:
            graph: The graph on which the ants are moving.
            pheromone: A dictionary containing pheromone levels for
                each edge in the graph.
            explored: A set of already explored nodes that allows
                the algorithm to guide the selection process more efficiently.
            current_node: The current node where the ant is located.
            alpha: The influence of the pheromone levels on the move decision.
            beta: The influence of the heuristic information (node degree)
                on the move decision.

        Returns:
            The next node to move to.
        """
        # retrieve edges connected to the current node
        edges = graph.edges(current_node)

        neighbors = []
        pheromone_list = []
        for edge in edges:
            neighbor = edge[1] if edge[0] == current_node else edge[0]
            neighbors.append(neighbor)
            # calulate pheromone values for each edge adjusted by
            # alpha parameter
            pheromone_value = get_pheromone_value(pheromone, edge) ** alpha
            pheromone_list.append(pheromone_value)

        pheromone_values = np.array(pheromone_list)

        # here we use the node degree heuristic
        # (number of edges connected to it)
        # this means that the nodes with fewer connections have a higher
        # heuristic value, the parameter beta controls the influence of this
        # heuristic i.e. a higher value of beta gives more importance to this
        # heuristic in the decision-making process for edge selection
        # calculate the heuristic value for each neighboring node adjusted by
        # beta
        attractiveness = np.array(
            [1.0 / graph.degree(neighbor) ** beta for neighbor in neighbors]
        )

        # use pheromone and attractiveness to calculate edge selection
        # probabilities
        probabilities = pheromone_values * attractiveness
        probabilities /= probabilities.sum()

        # we want to prioritize nodes that have not already been explored
        # only if all of them were explored so that we hit a dead end we
        # decide to choose an already explored node

        # filter out already explored nodes
        unexplored_neighbors = [n for n in neighbors if n not in explored]
        if unexplored_neighbors:
            unexplored_probabilities = np.array(
                [
                    probabilities[neighbors.index(n)]
                    for n in unexplored_neighbors
                ]
            )
            # normalize the remaining probability values so that the sigma
            # additivity holds for the entire sample space
            unexplored_probabilities /= unexplored_probabilities.sum()
            move = np.random.choice(
                unexplored_neighbors, p=unexplored_probabilities
            )
        else:
            move = np.random.choice(neighbors, p=probabilities)

        return move


class BasicPheromoneUpdate(PheromoneUpdateStrategy):
    def update_pheromone(
        self,
        pheromone: Dict[Tuple[int, int], float],
        paths: List[Tuple[List[int], int]],
        decay: float,
        n_best: int,
    ) -> Dict[Tuple[int, int], float]:
        """
        Updates the pheromone levels on the graph edges based on
        the paths found by the ants.

        Parameters:
            pheromone: A dictionary containing the current pheromone levels
                for each edge in the graph.
            paths: A list of tuples where each tuple contains a path and
                its length.
            decay: The decay factor applied to the pheromones to simulate
                evaporation.
            n_best: The number of best paths to consider for pheromone updates.

        Returns:
            The updated pheromone levels for each edge in the graph.
        """
        # sort paths by their length is ascending order
        sorted_paths = sorted(paths, key=lambda x: x[1])
        # update pheromone levels on the best paths
        # we add more pheromone to edges that are part of the
        # best paths found by the ants
        for path, length in sorted_paths[:n_best]:
            for move in zip(path[:-1], path[1:]):
                set_pheromone_value(
                    pheromone,
                    move,
                    get_pheromone_value(pheromone, move) + 1.0 / length,
                )
        # apply pheromone decay
        # reducing the pheromone levels on all edges to simulate
        # the natural evaporation of pheromones over time
        pheromone = {k: v * decay for k, v in pheromone.items()}
        return pheromone


# The necessity of this function stems from the way that NetworkX represents
# undirected graphs, where we are not sure whether the edge between two
# nodes u and v is stored as (u, v) or (v, u).
def get_pheromone_value(
    pheromone: Dict[Tuple[int, int], float], edge: Tuple[int, int]
) -> float:
    """
    Retrieve the pheromone value.

    Parameters:
        pheromone: Dictionary containg pheromone values for each edge.
        edge: Edge used for retrieval.

    Returns:
        Pheromone value for the edge.
    """
    u, v = edge
    return pheromone[(u, v)] if (u, v) in pheromone else pheromone[(v, u)]


# The reasoning is similar to get_pheromone_value function.
def set_pheromone_value(
    pheromone: Dict[Tuple[int, int], float],
    edge: Tuple[int, int],
    value: float,
):
    """
    Set the pheromone value provided.

    Parameters:
        pheromone: Dictionary containg pheromone values for each edge.
        edge: Edge used for updating.
        value: Value to set for the edge.
    """
    u, v = edge
    pheromone[(u, v) if (u, v) in pheromone else (v, u)] = value
