import networkx as nx
import pygame
def draw_maze(mst: nx.Graph, rows: int, cols: int, cell_size: int = 20):
    pygame.init()
    width, height = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze")
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill(white)

    walls = _gen_maze_walls(rows, cols)
    edges = [
        ((0, 0), (0, 1)),
        ((0, 1), (1, 1))
    ]
    # edges = mst.edges
    _remove_walls_with_graph_edges(edges, walls)




    for (u, v) in walls:
        x1, y1 = u[1] * cell_size, u[0] * cell_size
        x2, y2 = v[1] * cell_size, v[0] * cell_size
        pygame.draw.line(screen, black, (x1, y1), (x2, y2), 2)

    # pygame.draw.line()

    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


def _remove_walls_with_graph_edges(edges, walls):
    for u, v in edges:
        u, v = sorted((u, v))
        r1, r2 = u[0], v[0]
        c1, c2 = u[1], v[1]

        if r1 == r2:
            wall = ((r2, c2), (r2 + 1, c2))
        elif c1 == c2:
            wall = ((r2, c2), (r2, c2 + 1))
        else:
            raise AssertionError(f"Invalid edge {(u, v)}")
        walls.remove(wall)


def _gen_maze_walls(rows, cols):
    walls = [((row, col), (row, col + 1)) for row in range(rows)
             for col in range(cols)]
    walls.extend(
        [((row, col), (row + 1, col)) for row in range(rows)
         for col in range(cols)]
    )
    walls = set(walls)
    return walls