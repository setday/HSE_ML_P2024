import arcade
import numpy as np

from src.render.RenderGroup import RenderGroup


class GameOfLifeField:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

        # Initialize the game grid
        self.grid: np.ndarray = np.zeros((height, width))

    def update(self):
        new_grid: np.ndarray = self.grid.copy()

        for i in range(self.height):
            for j in range(self.width):
                state = self.grid[i, j]
                neighbours = (
                        np.sum(
                            self.grid[
                            max(0, i - 1): min(self.height, i + 2),
                            max(0, j - 1): min(self.width, j + 2),
                            ]
                        )
                        - state
                )

                if state and not 2 <= neighbours <= 3:
                    new_grid[i, j] = 0
                elif not state and neighbours == 3:
                    new_grid[i, j] = 1

        self.grid = new_grid

    def get_grid(self):
        return self.grid


class GameOfLifeScene:
    def __init__(self):
        self.render_group: RenderGroup = RenderGroup()

        self.RESOLUTION: int = 10
        self.ROWS, self.COLS = 500 // self.RESOLUTION, 500 // self.RESOLUTION

        self.field: GameOfLifeField = GameOfLifeField(self.COLS, self.ROWS)

        for i in range(self.ROWS):
            for j in range(self.COLS):
                if np.random.random() < 0.5:
                    self.field.grid[i, j] = 1

    def update(self, io_controller, delta_time):
        self.field.update()

        if not io_controller.mouse.get(1, False):
            return

        x, y = io_controller.mouse_position
        x -= 100
        y -= 100

        if x < 0 or y < 0 or x > 500 or y > 500:
            return

        self.field.grid[
            y // self.RESOLUTION, x // self.RESOLUTION
        ] = not self.field.grid[y // self.RESOLUTION, x // self.RESOLUTION]

    def draw(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.field.grid[i, j]:
                    arcade.draw_rectangle_filled(
                        j * self.RESOLUTION + 100,
                        i * self.RESOLUTION + 100,
                        self.RESOLUTION - 1,
                        self.RESOLUTION - 1,
                        arcade.color.WHITE,
                    )
                else:
                    arcade.draw_rectangle_filled(
                        j * self.RESOLUTION + 100,
                        i * self.RESOLUTION + 100,
                        self.RESOLUTION - 1,
                        self.RESOLUTION - 1,
                        arcade.color.BLACK,
                    )
        pass
