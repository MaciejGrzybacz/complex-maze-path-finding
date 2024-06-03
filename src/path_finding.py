"""
This module implements the ACO algorithm to find
the shortest path between to given nodes in a graph.
"""

import networkx as nx
from typing import List, Tuple

from .aco_strategies import MoveSelectionStrategy, PheromoneUpdateStrategy
from .aco_strategies import PheromoneBasedMoveSelection, BasicPheromoneUpdate

class AntColonyOptimization:
    
    def __init__(self, graph: nx.Graph, n_ants: int, n_best: int,
                 n_iterations: int, decay: float, alpha: float = 1,
                 beta: float = 1,
                 move_selection_strategy: MoveSelectionStrategy = None,
                 pheromone_update_strategy: PheromoneUpdateStrategy = None):
        """
        Initialize ACO algorithm with necessary parameters.
        
        Parameters:
            graph: The graph on which the ACO algorithm will run.
                The graph is converted to and undirected graph.
            n_ants: The number of ants used in each iteration.
            n_best: The number of best ants whose paths will be used
                to update the pheromone levels.
            n_iterations: The number of iterations the algorithm will run.
            decay: The rate at which the pheromone decays after each iteration.
            alpha: The influence of the pheromone levels on the move decision.
            beta: The influence of the heuristic information on the move decision.
            move_selection_strategy: The strategy used for selecting the next
                move for an ant.
            pheromone_update_strategy: The strategy used for updating the
                pheromone levels.
        """
        self.graph = graph.to_undirected()
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.pheromone = {edge: 1 for edge in self.graph.edges()}
        self.all_nodes = list(graph.nodes())
        self.move_selection_strategy = move_selection_strategy
        self.pheromone_update_strategy = pheromone_update_strategy
        
        # if no strategies are provided the default is used
        if move_selection_strategy is None:
            self.move_selection_strategy = PheromoneBasedMoveSelection()
        
        if pheromone_update_strategy is None:
            self.pheromone_update_strategy = BasicPheromoneUpdate()
    
    def run(self, start: int, end: int) -> Tuple[List[int], int]:
        """
        Run the ACO algorithm to find the shortest path from the start
        node to the end node.
        
        Parameters:
            start: The start node.
            end: The end node.
        
        Returns:
            A tuple containing the shortest path found and its length.
        """
        # shortest path found in each iteration
        shortest_path = None
        # shortest path found across all iterations
        all_time_shortest_path = ("placeholder", float("inf"))
        
        for _ in range(self.n_iterations):
            # construct a path for all ants from start to end
            all_paths = self._construct_colony_paths(start, end)
            # update the pheromone on the edges based on the paths
            # found by the ants
            self.pheromone = self.pheromone_update_strategy.update_pheromone(
                self.pheromone, all_paths, self.decay, self.n_best
            )
            # find the shortest path in the current iteration
            shortest_path = min(all_paths, key=lambda x: x[1])
            
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
        
        return all_time_shortest_path
    
    def _construct_colony_paths(self, start: int, end: int):
        """
        Constructs paths for all ants in the colony from the
        start node to the end node.
        
        Parameters:
            start: The start node.
            end: The end node.
            
        Returns:
            A list of tuples where each tuple contains a path and its length.
        """
        all_paths = []
        for _ in range(self.n_ants):
            path = self._construct_path(start, end)
            all_paths.append((path, AntColonyOptimization.path_length(path)))

        return all_paths
    
    def _construct_path(self, start: int, end: int) -> List[int]:
        """
        Constructs a single path for an ant from the start node
        to the end node.
        
        Parameters:
            start: The start node.
            end: The end node.
        
        Returns:
            The path constructed by the ant.
        """
        path = [start]
        # This set stored all the already explored nodes in the graph.
        # We are going to prioritize exploration of unexplored nodes.
        explored = {start} 
        while path[-1] != end:
            move = self.move_selection_strategy.select_move(
                self.graph, self.pheromone, explored,
                path[-1], self.alpha, self.beta
            )
            path.append(move)
            explored.add(move)
        
        return path
    
    @staticmethod
    def path_length(path: List[int]) -> int:
        """
        Calculates the length of a given path.
        
        Parameters:
            path: The path to calculate the length for.
            
        Returns:
            The length of the path.
        """
        return len(path) - 1
