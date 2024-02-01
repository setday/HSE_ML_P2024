import pygame
import pymunk

from src.game_engine.entities.Car import Car
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite


class GameScene:
    def __init__(self, window):
        self.window = window

        self.render_group = RenderGroup(window.width, window.height)
        self.space = pymunk.Space()

        self.background = BasicSprite("assets/Map.jpg", (400, 400), self.render_group)

        self.car = Car(self.render_group, self.space)
        self.render_group.snap_camera_to_sprite(self.car.car_view)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.car.turn_left(keys[pygame.K_SPACE])
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.car.turn_right(keys[pygame.K_SPACE])
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.car.accelerate()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.car.brake()
        if keys[pygame.K_r]:
            self.car.car_model.body.velocity = (0, 0)

        if keys[pygame.K_SPACE]:
            self.car.hand_brake()

        self.space.step(1 / 60)
        self.car.apply_friction()
        self.car.sync()

    def draw(self):
        pass
