"""
This module is the entry point for the application.
"""
from src.graph_generation import generate_maze_kruskal, draw_maze

if __name__ == "__main__":
    print("Hello ACO world!")
    rows, cols = 20, 20
    mst = generate_maze_kruskal(rows, cols)
    draw_maze(mst, rows, cols)
