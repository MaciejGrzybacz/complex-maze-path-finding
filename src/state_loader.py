"""
This module contains functions for retrieving ACO's
state from JSON files created by functions from
state_saver module.
"""

import json
from typing import List, Dict, Any

DEFAULT_FILE_PATH = "data/aco_state.jsonl"


def load_all_states(file_path: str) -> List[Dict[str, Any]]:
    """
    Load the states after all iterations from
    the JSON Lines file.

    Parameters:
        file_path: The path to the JSON Lines file.

    Returns:
        A list of dictionaries, each representing the
        state of one iteration.
    """
    states = []
    with open(file_path, mode="r") as file:
        for line in file:
            states.append(json.loads(line))

    return states


def load_state_by_iteration(file_path: str, iteration: int) -> Dict[str, Any]:
    """
    Load a specific iteration's state from the JSON Lines file.

    Parameters:
        file_path: The path to the JSON Lines file.
        iteration: The iteration number to retrieve.

    Returns:
        A dictionary representing the state of the specified iteration.
    """
    with open(file_path, mode="r") as file:
        for line in file:
            state = json.loads(line)
            if state["iteration"] == iteration:
                return state

    raise ValueError(f"Iteration {iteration} not found in {file_path}")


def filter_states(file_path: str, condition: Any) -> List[Dict[str, Any]]:
    """
    Load states that meet a specific condition from the JSON Lines file.

    Parameters:
        file_path: The path to the JSON Lines file.
        condition: A function that takes a state dictionary and returns True
            if it meets the condition.

    Returns:
        A list of dictionaries, each representing a state that meets the
            condition.
    """
    filtered_states = []

    with open(file_path, mode="r") as file:
        for line in file:
            state = json.loads(line)
            if condition(state):
                filtered_states.append(state)

    return filtered_states
