from arcade import load_font as arcade_load_font
from arcade import load_texture as arcade_load_texture
from pyglet.image import load as pyglet_load_image


def load_image(path: str):
    try:
        return pyglet_load_image(path)
    except Exception as e:
        print(f"While loading image at path: {path}, encountered exception: {e}")
        return pyglet_load_image("assets/missing.png")


def load_texture(path: str):
    try:
        return arcade_load_texture(path)
    except Exception as e:
        print(f"While loading texture at path: {path}, encountered exception: {e}")
        return arcade_load_texture("assets/missing.png")


def load_font(path: str):
    try:
        return arcade_load_font(path)
    except Exception as e:
        print(f"While loading font at path: {path}, encountered exception: {e}")
        return arcade_load_font("assets/fnt/ka1.ttf")
