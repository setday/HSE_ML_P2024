import arcade


class BasicDrawable(arcade.Sprite):
    def __init__(self, position):
        super().__init__()

        # self.rect = arcade.Rect(0, 0, 0, 0)
        # self.rect.center = position

        self.angle = 0
        self.position = position
        self.scale = 1

        # self.src_surface = None
        # self.surface = self.src_surface

    def update_position(self, position):
        self.position = position

    def update_angle(self, angle):
        self.angle = angle

        # self.surface = pygame.transform.rotate(self.src_surface, self.angle)
        # self.surface = pygame.transform.scale_by(self.surface, self.scale)
        # self.rect = self.surface.get_rect(center=self.position)

    def update_scale(self, scale):
        self.scale = scale

        # self.surface = pygame.transform.rotate(self.src_surface, self.angle)
        # self.surface = pygame.transform.scale_by(self.surface, self.scale)
        # self.rect = self.surface.get_rect(center=self.position)

    def draw_to(self, screen, position, size):
        arcade.draw_scaled_texture_rectangle(self.position[0], self.position[1], self.texture, self.scale, self.angle)
