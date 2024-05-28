from arcade import Texture
from arcade.gui import UIInteractiveWidget, Surface, UIEvent, UIMouseDragEvent, UIMousePressEvent


class UISlider(UIInteractiveWidget):
    """
    Slider widget

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param float width: width of widget
    :param float height: height of widget
    :param float value: value of the slider
    :param float min_value: minimum value of the slider
    :param float max_value: maximum value of the slider
    :param float step: step size of the slider
    :param str direction: direction of the slider (horizontal, vertical)
    :param style: style information for the slider.
    :param size_hint: Tuple of floats (0.0-1.0), how much space of the parent should be requested
    :param size_hint_min: min width and height in pixel
    :param size_hint_max: max width and height in pixel
    """

    def __init__(self,
                 textures: tuple[
                     Texture, Texture, Texture,
                     Texture, Texture, Texture,
                     Texture, Texture, Texture,
                     Texture
                 ],
                 x: float = 0,
                 y: float = 0,
                 width: float | None = None,
                 height: float | None = None,
                 scale: float | None = None,
                 value: int = 0,
                 change_callback: callable or None = None,
                 **kwargs):

        texture = textures[value]

        if width is None and texture is not None:
            width = texture.width

        if height is None and texture is not None:
            height = texture.height

        if scale is not None and texture is not None:
            height = texture.height * scale
            width = texture.width * scale

        super().__init__(x, y, width, height, **kwargs)

        self.value: int = value
        self.textures = textures

        self.scale = scale

        self._change_callback = change_callback

    def on_event(self, event: UIEvent) -> bool:
        if not self.pressed and isinstance(event, UIMousePressEvent):
            self.try_update_value(event.x)
        if self.pressed and isinstance(event, UIMouseDragEvent):
            self.try_update_value(event.x)

        return super().on_event(event)

    def try_update_value(self, x: float) -> bool:
        new_value = self.calc_new_value(x)

        if new_value != self.value:
            self.value = new_value

            if self._change_callback:
                self._change_callback(new_value)

            return True

        return False

    def calc_new_value(self, x: float) -> int:
        x -= self.x + 8 * self.scale
        x /= (self.width - 16 * self.scale)
        x *= 9

        new_value = round(x)
        new_value = min(max(new_value, 0), 9)

        return new_value

    def do_render(self, surface: Surface):
        self.prepare_render(surface)

        tex = self.textures[self.value]

        if tex:
            surface.draw_texture(0, 0, self.width, self.height, tex=tex)
