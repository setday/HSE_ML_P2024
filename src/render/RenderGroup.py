import pygame
import numpy as np


class RenderGroup(pygame.sprite.Group):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        self.width = width
        self.height = height

        self.position = pygame.math.Vector2(0, 0)
        self.zoom = 1

        self.target_position = pygame.math.Vector2(0, 0)
        self.target_zoom = 1

        self.screen_shift = pygame.math.Vector2(self.width / 2, self.height / 2)

        self.snapped_sprite = None

    def set_camera_position(self, position: pygame.math.Vector2) -> None:
        self.target_position = position

    def set_camera_zoom(self, zoom: float) -> None:
        self.target_zoom = zoom

        for sprite in self.sprites():
            sprite.update_scale(zoom)

    def snap_camera_to_sprite(self, sprite: pygame.sprite.Sprite) -> None:
        self.snapped_sprite = sprite

    def update(self):
        if self.snapped_sprite is not None:
            self.set_camera_position(self.snapped_sprite.position)

        self.position += (self.target_position - self.position) * 0.003
        self.zoom += (self.target_zoom - self.zoom) * 0.003

    def custom_draw(self, screen: pygame.Surface) -> None:
        for sprite in self.sprites():
            sprite.draw_to(screen, self.position * self.zoom - self.screen_shift, self.zoom)
