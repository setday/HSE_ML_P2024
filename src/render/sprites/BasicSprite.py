import arcade

from src.render.sprites.BasicDrawable import BasicDrawable


class BasicSprite(BasicDrawable):
    def __init__(self, image, position):
        super().__init__(position)

        self.cnt1 = 0
        self.cnt2 = 0

        self.src_surface = arcade.load_texture(image)

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(1)
