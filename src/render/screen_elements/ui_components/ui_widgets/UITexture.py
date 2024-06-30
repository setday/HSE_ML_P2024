from arcade import Texture
from arcade.gui import UIWidget
from arcade.gui.surface import Surface


class UITexture(UIWidget):
    """
    Texture widget

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param float width: width of widget. Defaults to texture width if not specified.
    :param float height: height of widget. Defaults to texture height if not specified.
    :param Texture texture: texture to display for the widget.
    :param Texture texture_hovered: different texture to display if mouse is hovering over button.
    :param Texture texture_pressed: different texture to display if mouse button is pressed while hovering over button.
    :param str text: text to add to the button.
    :param style: style information for the button.
    :param float scale: scale the button, based on the base texture size.
    :param size_hint: Tuple of floats (0.0-1.0), how much space of the parent should be requested
    :param size_hint_min: min width and height in pixel
    :param size_hint_max: max width and height in pixel
    """

    def __init__(
        self,
        child: UIWidget | None = None,
        x: float = 0.0,
        y: float = 0.0,
        width: float = None,
        height: float = None,
        texture: Texture | None = None,
        scale: float | None = None,
        **kwargs
    ):

        if width is None and texture is not None:
            width = texture.width

        if height is None and texture is not None:
            height = texture.height

        if scale is not None and texture is not None:
            height = texture.height * scale
            width = texture.width * scale

        children = []
        if child:
            children.append(child)

        super().__init__(x, y, width, height, children, **kwargs)

        self._tex = texture

    def do_render(self, surface: Surface):
        self.prepare_render(surface)
        surface.draw_texture(0, 0, self.width, self.height, tex=self._tex)
