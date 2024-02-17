import pygame
import pymunk

from src.game_engine.entities.Button import Button
from src.game_engine.entities.Car import Car
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.game_engine.entities.Obstacle import Obstacle
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite
from random import randint


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

        self.background = BasicSprite("../assets/Map2.jpg", (300, 400))
        self.create_park_places()
        self.render_group.add(self.background)

        self.car = Car(self.render_group, self.space, (400, 350))
        self.car_2 = Car(self.render_group, self.space, (400, 300))
        self.render_group.snap_camera_to_sprite(self.car.car_view)
        self.generate_button = Button()

    def create_park_places(self):
        for i in range(1, 6):
            ParkingPlace(self.render_group, (i * 125, 0))

    def create_random_obstacles(self, num_obst):
        for i in range(num_obst):
            Obstacle(self.render_group, (randint(0, 800), randint(0, 800)))

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
        self.generate_button.draw(5, 5, self.create_random_obstacles, self.window.get_screen())
        pygame.display.update()
