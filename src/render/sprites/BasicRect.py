from typing import Tuple

from arcade import Texture

from src.render.sprites.BasicDrawable import BasicDrawable


class BasicRect(BasicDrawable):
    def __init__(self, width: int, height: int, position):
        super().__init__(position)

        self.width = int(width)
        self.height = int(height)

        self.color = (255, 255, 255)

        self.src_surface = Texture.create_filled(
            hash(self).__str__(), (width, height), (0, 0, 0)
        )
        self.texture = self.src_surface

        self.border_width = 2

        self._top_bottom_skip = 0
        self._center_horizontal_skip = 0
        self._center_vertical_skip = 0

        self.set_border_width(self.border_width)

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(1)

    def set_border_width(self, border_width: int) -> None:
        self.border_width = border_width

        self._top_bottom_skip = int(self.width * self.border_width)
        self._center_horizontal_skip = int(self.width - 2 * self.border_width)
        self._center_vertical_skip = int(self.height - 2 * self.border_width)

        self.update_color(self.color)

    def update_color(
        self, color: Tuple[int, int, int] | Tuple[int, int, int, int]
    ) -> None:
        self.color = color

        data = (
            [color] * self._top_bottom_skip
            + (
                [color] * self.border_width
                + [(0, 0, 0, 0)] * max(0, self._center_horizontal_skip)
                + [color] * self.border_width
            )
            * max(0, self._center_vertical_skip)
            + [color] * self._top_bottom_skip
        )

        self.src_surface.image.putdata(data)
        self.texture = self.src_surface
