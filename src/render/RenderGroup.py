import pygame
import numpy as np


class RenderGroup(pygame.sprite.Group):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.position = pygame.math.Vector2(0, 0)
        self.zoom = 1

        self.target_position = pygame.math.Vector2(0, 0)

        self.snapped_sprite = None

    def set_camera_position(self, position):
        self.target_position = position - pygame.math.Vector2(self.width / 2, self.height / 2)

    def set_camera_zoom(self, zoom):
        self.zoom = zoom

    def snap_camera_to_sprite(self, sprite):
        self.snapped_sprite = sprite

    def update(self):
        if self.snapped_sprite is not None:
            self.set_camera_position(self.snapped_sprite.position)

        self.position += (self.target_position - self.position) * 0.003
        self.zoom = self.zoom

    def custom_draw(self, screen):
        for sprite in self.sprites():
            screen.blit(sprite.image, self.__apply_transforms(sprite.rect))

    def __apply_transforms(self, rect):
        return rect.move(-self.position.x, -self.position.y).scale_by(self.zoom, self.zoom)
