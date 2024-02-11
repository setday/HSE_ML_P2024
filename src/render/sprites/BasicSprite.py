import pygame

from src.render.sprites.BasicDrawable import BasicDrawable


class BasicSprite(BasicDrawable):
    def __init__(self, image, position, group):
        super().__init__(position, group)

        self.cnt1 = 0
        self.cnt2 = 0

        self.src_surface = pygame.image.load(image)

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(1)
