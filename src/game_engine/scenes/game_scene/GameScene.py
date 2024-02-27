import time

import pygame
import pymunk

from src.game_engine.entities.Car import Car
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
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
        self.score = 10000

        self.prev_time = time.time()

        def collision_car_with_car(arbiter, space, data):
            car1: Car = arbiter.shapes[0].super
            car2: Car = arbiter.shapes[1].super

            delta_score = (car1.car_model.body.velocity - car2.car_model.body.velocity).get_length_sqrd() / 30
            self.score -= delta_score

            health_decreation = max(0, delta_score - 1)
            car1.health -= health_decreation
            car2.health -= health_decreation

            return True

        def collision_car_with_O(arbiter, space, data):
            car: Car = arbiter.shapes[0].super

            self.score -= 10

            return True

        h = self.space.add_collision_handler(10, 10)
        h.begin = collision_car_with_car
        h = self.space.add_collision_handler(10, 20)
        h.begin = collision_car_with_O
        h = self.space.add_collision_handler(10, 30)
        h.begin = collision_car_with_O

        self.background = BasicSprite("assets/Map.jpg", (0, 0))
        self.background.update_scale(10)

        self.render_group.add(self.background)

        self.car_m = Car(self.render_group, self.space, (0, -100), 0)
        self.cars = [self.car_m]
        for i in range(-5, 5):
            if i == 0:
                continue
            self.cars.append(Car(self.render_group, self.space, (70 * i, -100), 1))

        self.traffic_cones = []
        for i in range(-5, 5):
            self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * i, -170)))

        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * -5 - 35, -70)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * -5 - 40, -100)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * -5 - 35, -130)))

        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * 4 + 35, -70)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * 4 + 40, -100)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * 4 + 35, -130)))

        for i in range(-5, 5):
            StaticObstacle(self.render_group, self.space, (70 * i, -10))

        self.render_group.snap_camera_to_sprite(self.car_m.car_view)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.car_m.turn_left(keys[pygame.K_SPACE])
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.car_m.turn_right(keys[pygame.K_SPACE])
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.car_m.accelerate()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.car_m.brake()
        if keys[pygame.K_r]:
            self.car_m.car_model.body.velocity = (0, 0)

        if keys[pygame.K_SPACE]:
            self.car_m.hand_brake()

        for car in self.cars:
            if car == self.car_m:
                continue
            # car.hand_brake()

        current_time = time.time()
        delta_time = current_time - self.prev_time
        self.prev_time = current_time

        delta_time *= 16

        self.space.step(delta_time)
        self.clock.tick(delta_time * 60000)

        for car in self.cars:
            car.apply_friction()
            car.sync()

        for cone in self.traffic_cones:
            cone.apply_friction()
            cone.sync()

        # self.render_group.set_camera_zoom(1 / (1 + self.car.car_model.body.velocity.get_length_sqrd() / 10000))

    def draw(self):
        pass
        # self.cnt += 1
        # if self.cnt % 30 == 0:
            # print(str(self.clock.get_fps()))
        # self.window.get_screen().blit(
        #     self.font.render(
        #         str(int(self.clock.get_fps())),
        #         1, pygame.Color("GREEN")
        #     ), (0, 0)
        # )
