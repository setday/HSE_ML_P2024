import random
import time

import arcade
import pymunk

from src.game_engine.entities.Car import Car
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite
from src.game_engine.controllers.Controller import *


class GameScene:
    def __init__(self):
        self.render_group = RenderGroup()
        self.space = pymunk.Space()

        self.score = 10000

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
        self.car_m.switch_controller(KeyboardController())
        self.cars = [self.car_m]
        for i in range(-5, 5):
            if i == 0:
                continue
            car = Car(self.render_group, self.space, (70 * i, -100), 1)
            car.switch_controller(random.choice([RandomController(), AIController(), BrakeController()]))
            self.cars.append(car)

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

        self.render_group.camera.snap_to_sprite(self.car_m.car_view)

    def update(self, keys, delta_time):
        self.car_m.controlling(keys)

        for car in self.cars:
            if car == self.car_m:
                continue
            car.controlling(keys)

        delta_time *= 16

        self.space.step(delta_time)

        for car in self.cars:
            car.apply_friction()
            car.sync()

        for cone in self.traffic_cones:
            cone.apply_friction()
            cone.sync()

        self.render_group.camera.set_zoom(1 + self.car_m.car_model.body.velocity.get_length_sqrd() / 10000)

    def draw(self):
        self.render_group.draw()

        self.render_group.camera.use()
