import arcade

from pymunk import Vec2d as Vector2D


class BasicDrawable(arcade.Sprite):
    def __init__(self, position: Vector2D):
        super().__init__()

        self.texture = arcade.Texture.create_empty("WT", (1, 1))

        self.angle = 0
        self.position = position
        self.scale = 1

    def update_position(self, position: Vector2D) -> None:
        def inverse_y(pos: Vector2D) -> Vector2D:
            x, y = pos
            return Vector2D(x, -y)

        self.position = inverse_y(position)

    def update_angle(self, angle: float) -> None:
        self.angle = -angle

    def update_scale(self, scale: float) -> None:
        self.scale = scale
