import arcade

from pyglet.math import Vec2 as Vector2D

from src.render.sprites.BasicDrawable import BasicDrawable


class BasicSprite(BasicDrawable):
    def __init__(self, image, position: Vector2D = Vector2D(0, 0), scale=1) -> None:
        super().__init__(position)

        self.texture = arcade.load_texture(image)

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(scale)
