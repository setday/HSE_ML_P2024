import random

import pygame
import pymunk

from src.render.RenderGroup import RenderGroup


class PhysicScene:
    def __init__(self, window):
        self.window = window

        self.render_group = RenderGroup(window.width, window.height)

        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()
        self.space.gravity = (0, -1000)

        self.ground = pymunk.Segment(self.space.static_body, (0, 100), (600, 100), 1)
        self.ground.elasticity = 0.95
        self.space.add(self.ground)

        self.ball_mass = 1
        self.ball_radius = 30
        self.moment = pymunk.moment_for_circle(self.ball_mass, 0, self.ball_radius)
        self.ball_body = pymunk.Body(self.ball_mass, self.moment)
        self.ball_body.position = (300, 300)
        self.ball_shape = pymunk.Circle(self.ball_body, self.ball_radius)
        self.ball_shape.elasticity = 0.95
        self.space.add(self.ball_body, self.ball_shape)

    def update(self):
        self.clock.tick(60)
        self.space.step(1 / 60)

        # Randomly add impulse to ball
        if pygame.mouse.get_pressed()[0]:
            self.ball_body.apply_impulse_at_local_point((random.randint(-100, 100), random.randint(0, 100)))

        # Randomly add force to ball
        if pygame.mouse.get_pressed()[2]:
            self.ball_body.apply_force_at_local_point((0, 1000), (0, 0))

        # If k pressed half the speed of the ball
        if pygame.key.get_pressed()[pygame.K_k]:
            angle = 180
            rad = angle * 3.14 / 180
            self.ball_body.velocity = self.ball_body.velocity.rotated(rad)

    def draw(self):
        # Draw ground
        # pygame.draw.line(screen, (0, 0, 0), (0, 600 - 100), (600, 600 - 100), 2)

        # Draw ball
        # x, y = ball_body.position
        # pygame.draw.circle(screen, (0, 0, 255), (int(x), 600-int(y)), ball_radius)
        pass
