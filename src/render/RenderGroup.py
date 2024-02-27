import arcade

from src.render.Camera import Camera


class RenderGroup(arcade.Scene):
    def __init__(self) -> None:
        super().__init__()

        self.camera = Camera()

    def add(self, sprite: arcade.Sprite) -> None:
        self.add_sprite(hash(sprite).__str__(), sprite)
