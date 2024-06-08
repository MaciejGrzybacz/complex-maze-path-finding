import json
from typing import List, Tuple, Dict


def save_state(
    iteration: int,
    pheromone: Dict[Tuple[int, int], float],
    all_paths: List[Tuple[List[int], int]],
    shortest_path: Tuple[List[int], int],
    filepath: str = "aco_state.json"
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
    state = {
        "iteration": iteration,
        "pheromone": {f"{k[0]}-{k[1]}": v for k, v in pheromone.items()},
        "all_paths": [
            {"path": path, "length": length} for path, length in all_paths
        ],
        "shortest_path": {"path": shortest_path[0], "length": shortest_path[1]}
    }
    
    with open(filepath, mode="a") as file:
        file.write(json.dumps(state) + "\n")
