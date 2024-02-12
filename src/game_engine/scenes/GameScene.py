import pygame
import pymunk

from src.game_engine.entities.Car import Car
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite


class GameScene:
    def __init__(self, window):
        self.cnt = 0

        self.window = window

        self.render_group = RenderGroup(window.width, window.height)
        self.space = pymunk.Space()

        self.clock = pygame.time.Clock()

        # self.font = pygame.font.SysFont('Consolas', 18, bold=True)

        def collision_detecter(arbiter, space, data):
            print('Bah')
            return True

        h = self.space.add_collision_handler(0, 0)
        h.begin = collision_detecter

        self.background = BasicSprite("assets/Map.jpg", (300, 400))

        self.render_group.add(self.background)

        self.car = Car(self.render_group, self.space, (400, 350))
        self.car_2 = Car(self.render_group, self.space, (400, 300))
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
        self.clock.tick(10000)
        self.car.apply_friction()
        self.car_2.apply_friction()
        self.car.sync()
        self.car_2.sync()

        # self.render_group.set_camera_zoom(1 / (1 + self.car.car_model.body.velocity.get_length_sqrd() / 10000))

    def draw(self):
        pass
        # self.cnt += 1
        # if self.cnt % 30 == 0:
            # print(str(self.clock.get_fps()))
        # self.window.get_screen().blit(
        #     self.font.render(
        #         str(int(self.clock.get_fps())),
        #         1, pygame.Color("RED")
        #     ), (0, 0)
        # )
