import arcade

from pyglet.math import Vec2 as Vector2D


class BasicDrawable(arcade.Sprite):
    def __init__(self, position: Vector2D | tuple[float, float] = (0, 0)):
        super().__init__()

        self.texture = arcade.Texture.create_empty("WT", (1, 1))

        self.angle = 0
        self.position = Vector2D(0, 0)
        self.scale = 1

        self.update_position(position)

    def update_position(self, position: Vector2D | tuple[float, float]) -> None:
        def inverse_y(pos: Vector2D | tuple[float, float]) -> Vector2D:
            x, y = pos
            return Vector2D(x, -y)

        self.position = inverse_y(position)

    @property
    def x(self) -> float:
        return self.center_x

    @x.setter
    def x(self, value: float) -> None:
        self.center_x = value

    @property
    def y(self) -> float:
        return self.center_y

    @y.setter
    def y(self, value: float) -> None:
        self.center_y = -value

    def update_angle(self, angle: float) -> None:
        self.angle = -angle

    def update_scale(self, scale: float) -> None:
        self.scale = scale
