from typing import Optional, List

import arcade

from src.render.Camera import Camera


class RenderGroup(arcade.Scene):
    def __init__(self) -> None:
        super().__init__()

        self.camera = Camera()

    def add(self, sprite: arcade.Sprite) -> None:
        if isinstance(sprite, arcade.Sprite):
            self.add_sprite(hash(sprite).__str__(), sprite)
        elif isinstance(sprite, arcade.SpriteList):
            self.add_sprite_list(hash(sprite).__str__(), sprite_list=sprite)
        else:
            raise ValueError(f"Invalid sprite type: {type(sprite)}")

    def draw(self, names: Optional[List[str]] = None, **kwargs) -> None:
        kwargs["pixelated"] = kwargs.get("pixelated", True)
        super().draw(names, **kwargs)
