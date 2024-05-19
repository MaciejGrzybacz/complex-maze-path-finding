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
    for (u, v) in mst.edges():
        x1, y1 = u[1] * cell_size, u[0] * cell_size
        x2, y2 = v[1] * cell_size, v[0] * cell_size
        pygame.draw.line(screen, black, (x1, y1), (x2, y2), 2)

    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

