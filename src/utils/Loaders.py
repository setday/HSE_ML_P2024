from arcade import load_font as arcade_load_font
from arcade import load_texture as arcade_load_texture
from arcade.texture import Texture
from pyglet.image import AbstractImage
from pyglet.image import load as pyglet_load_image

from src.render.MimicTexture import texture_to_mimic


def load_image(path: str) -> AbstractImage:
    """
    @brief: Load an image from disk. (Pyglet)
    @param path: Path to the image file on disk.
    @return: Image object.
    """
    try:
        return pyglet_load_image(path)
    except Exception as e:
        print(f"While loading image at path: {path}, encountered exception: {e}")
        return pyglet_load_image("assets/missing.png")


def load_texture(path: str, pixelated: bool = True, **kwargs) -> Texture:
    """
    @brief: Load an image from disk and create a texture. (Arcade)
    @param path: Path to the image file on disk.
    @param pixelated: If True, the texture will be pixelated.
    @return: Texture object.
    """
    try:
        texture = arcade_load_texture(path, **kwargs)
        texture_to_mimic(texture, pixelated)
        return texture
    except Exception as e:
        print(f"While loading texture at path: {path}, encountered exception: {e}")
        texture = arcade_load_texture("assets/missing.png")
        texture_to_mimic(texture, pixelated)
        return texture


def load_font(path: str) -> None:
    """
    @brief: Load a font from disk. (Arcade)
    @param path: Path to the font file on disk.
    @return: Font object.
    """
    try:
        arcade_load_font(path)
    except Exception as e:
        print(f"While loading font at path: {path}, encountered exception: {e}")
        arcade_load_font("assets/fnt/ka1.ttf")
