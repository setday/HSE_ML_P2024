import arcade

from src.render.sprites.BasicDrawable import BasicDrawable


class BasicRect(BasicDrawable):
    def __init__(self, width: int, height: int, position):
        super().__init__(position)

        self.width = width
        self.height = height

        self.border_width = 2

        self.src_surface = arcade.Texture.create_filled(hash(self), (self.width, self.height), (0, 0, 0, 0))
        self.update_color((0, 255, 0))

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(1)

    def update_color(self, color):
        self.color = color

        top_bottom_skip = int(self.width * self.border_width)
        center_horizontal_skip = int(self.width - 2 * self.border_width)
        center_vertical_skip = int(self.height - 2 * self.border_width)

        data = [color] * top_bottom_skip + \
               ([color] * self.border_width + \
                [(0, 0, 0, 0)] * max(0, center_horizontal_skip) + \
                [color] * self.border_width) * max(0, center_vertical_skip) + \
               [color] * top_bottom_skip

        self.src_surface.image.putdata(data)
        self.texture = self.src_surface
