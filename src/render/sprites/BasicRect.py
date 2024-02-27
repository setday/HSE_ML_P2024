import pygame

from src.render.sprites.BasicDrawable import BasicDrawable


class BasicRect(BasicDrawable, pygame.Surface):
    def __init__(self, width, height, position):
        super().__init__(position)

        self.rect = pygame.Rect(0, 0, width, height)

        self.color = (0, 255, 0)

        self.src_surface = pygame.Surface((width, height))
        self.src_surface.fill(self.color)
        self.src_surface.set_colorkey((0, 0, 0))

        self.src_surface_inner = pygame.Surface((width - 4, height - 4))
        self.src_surface_inner.fill((0, 0, 0))

        self.src_surface.blit(self.src_surface_inner, (2, 2))

        self.update_position(position)
        self.update_angle(0)
        self.update_scale(1)

    def update_color(self, color):
        self.color = color
        self.src_surface.fill(self.color)
        self.src_surface.blit(self.src_surface_inner, (2, 2))
        self.update_angle(self.angle)
        self.update_scale(self.scale)
