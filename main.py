"""
This module is the entry point for the application.
"""
from src.display_maze import draw_maze
from src.graph_generation import generate_maze

if __name__ == "__main__":
    print("Hello ACO world!")
    rows, cols = 20, 20
    mst = generate_maze(rows, cols)
    draw_maze(mst, rows, cols)
