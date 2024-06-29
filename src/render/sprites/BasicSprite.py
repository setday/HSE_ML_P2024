from pyglet.math import Vec2 as Vector2D

from src.utils import load_texture
from .BasicDrawable import BasicDrawable


class BasicSprite(BasicDrawable):
    def __init__(
        self,
        image: str,
        position: Vector2D | tuple[float, float] = Vector2D(0, 0),
        scale: float = 1,
    ) -> None:
        super().__init__(position)

        self.texture = load_texture(image)

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(scale)
