from typing import Tuple

from arcade import Texture

from src.render.sprites.BasicDrawable import BasicDrawable


class BasicRect(BasicDrawable):
    def __init__(self, width: int, height: int, position):
        super().__init__(position)

        self.width = int(width)
        self.height = int(height)

        self.border_width = 2

        self._top_bottom_skip = int(width * self.border_width)
        self._center_horizontal_skip = int(width - 2 * self.border_width)
        self._center_vertical_skip = int(height - 2 * self.border_width)

        self.src_surface = Texture.create_filled(hash(self).__str__(), (width, height), (0, 0, 0))
        self.texture = self.src_surface
        self.update_color((255, 255, 255))

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(1)

    def update_color(self, color: Tuple[int, int, int] | Tuple[int, int, int, int]) -> None:
        self.color = color

        data = [color] * self._top_bottom_skip + (
                [color] * self.border_width +
                [(0, 0, 0, 0)] * max(0, self._center_horizontal_skip) +
                [color] * self.border_width
        ) * max(0, self._center_vertical_skip) + [color] * self._top_bottom_skip

        self.src_surface.image.putdata(data)
        self.texture = self.src_surface
