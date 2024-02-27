import arcade


class BasicDrawable(arcade.Sprite):
    def __init__(self, position):
        super().__init__()

        self.texture = arcade.Texture.create_empty("WT", (1, 1))

        self.angle = 0
        self.position = position
        self.scale = 1

    def update_position(self, position):
        self.position = position

    def update_angle(self, angle):
        self.angle = angle

    def update_scale(self, scale):
        self.scale = scale
