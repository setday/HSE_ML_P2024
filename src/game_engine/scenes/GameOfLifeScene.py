import numpy as np
import pygame

from src.render.RenderGroup import RenderGroup


class GameOfLifeField:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Initialize the game grid
        self.grid = np.zeros((height, width))

    def update(self):
        new_grid = self.grid.copy()

        for i in range(self.height):
            for j in range(self.width):
                state = self.grid[i, j]
                neighbours = np.sum(
                    self.grid[max(0, i - 1):min(self.height, i + 2), max(0, j - 1):min(self.width, j + 2)]) - state

                if state and not 2 <= neighbours <= 3:
                    new_grid[i, j] = 0
                elif not state and neighbours == 3:
                    new_grid[i, j] = 1

        self.grid = new_grid

    def get_grid(self):
        return self.grid


class GameOfLifeScene:
    def __init__(self, window):
        self.window = window

        self.render_group = RenderGroup(window.width, window.height)

        self.RESOLUTION = 10
        self.ROWS, self.COLS = window.height // self.RESOLUTION, window.width // self.RESOLUTION

        self.field = GameOfLifeField(self.COLS, self.ROWS)
        self.grid = self.field.get_grid()

        for i in range(self.ROWS):
            for j in range(self.COLS):
                if np.random.random() < 0.5:
                    self.grid[i, j] = 1

        # for i in range(self.ROWS):
        #     for j in range(self.COLS):
        #         pygame.sprite.(screen, (0, 0, 0),
        #                          (j * RESOLUTION, i * RESOLUTION, RESOLUTION - 1, RESOLUTION - 1))

    def update(self):
        self.field.update()

        x, y = pygame.mouse.get_pos()
        self.grid[y // self.RESOLUTION, x // self.RESOLUTION] = not self.grid[
            y // self.RESOLUTION, x // self.RESOLUTION]

    def draw(self):
        # for i in range(self.ROWS):
        #     for j in range(self.COLS):
        #         if self.grid[i, j]:
        #             pygame.draw.rect(screen, (255, 255, 255),
        #                              (j * self.RESOLUTION, i * self.RESOLUTION, self.RESOLUTION - 1, self.RESOLUTION - 1))
        #         else:
        #             pygame.draw.rect(screen, (0, 0, 0),
        #                              (j * self.RESOLUTION, i * self.RESOLUTION, self.RESOLUTION - 1, self.RESOLUTION - 1))
        pass
