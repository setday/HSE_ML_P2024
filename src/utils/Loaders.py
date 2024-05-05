from pyglet.image import load as pyglet_load_image
from arcade import load_texture as arcade_load_texture
from arcade import load_font as arcade_load_font


def load_image(path: str):
    try:
        return pyglet_load_image(path)
    except:
        print(f"Failed to load image at path: {path}")
        return pyglet_load_image("assets/missing.png")


def load_texture(path: str):
    try:
        return arcade_load_texture(path)
    except:
        print(f"Failed to load texture at path: {path}")
        return arcade_load_texture("assets/missing.png")


def load_font(path: str):
    try:
        return arcade_load_font(path)
    except:
        print(f"Failed to load font at path: {path}")
        return arcade_load_font("assets/fnt/ka1.ttf")
