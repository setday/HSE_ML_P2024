from typing import Optional

import PIL.Image
from arcade.texture import Texture


class MimicTexture(Texture):
    """
    MimicTexture class is used to mimic the Texture class from arcade.texture.Texture with extra functionality.
    Pixelation is supported by this class.
    """

    def __init__(
        self,
        name: str,
        image: PIL.Image.Image = None,
        hit_box_algorithm: Optional[str] = "Simple",
        hit_box_detail: float = 4.5,
        pixelated: bool = True,
    ):
        super().__init__(name, image, hit_box_algorithm, hit_box_detail)

        self.pixelated = pixelated

    def draw_sized(
        self,
        center_x: float,
        center_y: float,
        width: float,
        height: float,
        angle: float = 0,
        alpha: int = 255,
    ):
        """Draw a texture with a specific width and height."""

        self._create_cached_sprite()
        if self._sprite and self._sprite_list:
            self._sprite.center_x = center_x
            self._sprite.center_y = center_y
            self._sprite.height = height
            self._sprite.width = width
            self._sprite.angle = angle
            self._sprite.alpha = alpha
            self._sprite_list.draw(pixelated=self.pixelated)

    def draw_scaled(
        self,
        center_x: float,
        center_y: float,
        scale: float = 1.0,
        angle: float = 0,
        alpha: int = 255,
    ):
        """
        Draw the texture.

        :param float center_x: X location of where to draw the texture.
        :param float center_y: Y location of where to draw the texture.
        :param float scale: Scale to draw rectangle. Defaults to 1.
        :param float angle: Angle to rotate the texture by.
        :param int alpha: The transparency of the texture `(0-255)`.
        """

        self._create_cached_sprite()
        if self._sprite and self._sprite_list:
            self._sprite.center_x = center_x
            self._sprite.center_y = center_y
            self._sprite.scale = scale
            self._sprite.angle = angle
            self._sprite.alpha = alpha
            self._sprite_list.draw(pixelated=self.pixelated)


def texture_to_mimic(texture: Texture, pixelated: bool = True) -> None:
    """
    Add specific methods and attributes to the texture object to make it work like a MimicTexture object.
    @param texture: texture object to make mimic.
    @param pixelated: whether to pixelate the texture or not.
    @return: None
    """
    texture.pixelated = pixelated
    texture.__class__ = MimicTexture
