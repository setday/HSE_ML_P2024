import pygame
import numpy as np

def run_game():
    # Set up some constants
    WIDTH, HEIGHT = 800, 800
    RESOLUTION = 10
    ROWS, COLS = HEIGHT // RESOLUTION, WIDTH // RESOLUTION

    # Initialize the game grid
    grid = np.zeros((ROWS, COLS))

    def draw_grid():
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i, j]:
                    pygame.draw.rect(screen, (255, 255, 255), (j*RESOLUTION, i*RESOLUTION, RESOLUTION-1, RESOLUTION-1))
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (j*RESOLUTION, i*RESOLUTION, RESOLUTION-1, RESOLUTION-1))

    def update_grid(grid):
        new_grid = grid.copy()
        for i in range(ROWS):
            for j in range(COLS):
                state = grid[i, j]
                neighbours = np.sum(grid[max(0, i-1):min(ROWS, i+2), max(0, j-1):min(COLS, j+2)]) - state
                if state and not 2 <= neighbours <= 3:
                    new_grid[i, j] = 0
                elif not state and neighbours == 3:
                    new_grid[i, j] = 1
        return new_grid

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True

    for i in range(ROWS):
        for j in range(COLS):
            if np.random.random() < 0.5:
                grid[i, j] = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid[y//RESOLUTION, x//RESOLUTION] = not grid[y//RESOLUTION, x//RESOLUTION]
        screen.fill((0, 0, 0))
        draw_grid()
        grid = update_grid(grid)
        pygame.display.update()

    pygame.quit()
