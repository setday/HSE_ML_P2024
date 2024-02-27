import pygame


class BasicDrawable(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = position

        self.angle = 0
        self.position = position
        self.scale = 1

        self.src_surface = None
        self.surface = self.src_surface

    def update_position(self, position):
        self.rect.center = self.position = position

    def update_angle(self, angle):
        self.angle = angle

        self.surface = pygame.transform.rotate(self.src_surface, self.angle)
        self.surface = pygame.transform.scale_by(self.surface, self.scale)
        self.rect = self.surface.get_rect(center=self.position)

    def update_scale(self, scale):
        self.scale = scale

        self.surface = pygame.transform.rotate(self.src_surface, self.angle)
        self.surface = pygame.transform.scale_by(self.surface, self.scale)
        self.rect = self.surface.get_rect(center=self.position)

    def draw_to(self, screen, position, size):
        rect_cpy = self.rect.copy()
        rect_cpy.center = pygame.math.Vector2(self.position) * size - position
        screen.blit(self.surface, rect_cpy)
