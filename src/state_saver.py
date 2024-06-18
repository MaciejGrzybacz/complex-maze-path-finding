"""
This module contains functions for saving the state
of the algorithm after each iteration into files.
"""

import json
from typing import List, Tuple, Dict
import os


def save_state(
    iteration: int,
    pheromone: Dict[Tuple[int, int], float],
    all_paths: List[Tuple[List[int], int]],
    shortest_path: Tuple[List[int], int],
    filepath: str = "aco_state.json",
):
    """
    Saves the state of the algorithm after an iteration
    as a JSON object.

    Parameters:
        iteration: The number of the iteration.
        pheromone: Pheromone levels for the edges.
        all_paths: All paths found by the ants.
        shortest_path: The shortest path found.
        filepath: Path to the JSON file.
    """
    # Convert values to standard Python data types
    pheromone_values = {
        f"{k[0]}-{k[1]}": float(v) for k, v in pheromone.items()
    }

    all_paths_values = [
        {"path": [int(node) for node in path], "length": int(length)}
        for path, length in all_paths
    ]

    shortest_path_values = {
        "path": [int(node) for node in shortest_path[0]],
        "length": int(shortest_path[1]),
    }

    state = {
        "iteration": iteration,
        "pheromone": pheromone_values,
        "all_paths": all_paths_values,
        "shortest_path": shortest_path_values,
    }

    if not os.path.isdir("data"):
        os.mkdir("data")

    with open(filepath, mode="a") as file:
        file.write(json.dumps(state) + "\n")
