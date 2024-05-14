import arcade.key
import numpy as np

from src.game_engine.Core import Core
from src.render.Window import IOController


class Game:
    def __init__(self):
        self.core = Core()
        self.time = 0

    def observe(self):
        car_pos = self.core.scene.car_m.car_model.body.position
        car_angle = self.core.scene.car_m.car_model.body.angle
        car_speed = (
            self.core.scene.car_m.car_model.body.velocity.get_length_sqrd() ** 0.5
        )
        pp_pos = self.core.scene.parking_place.parking_model.inner_body.position
        pp_angle = self.core.scene.parking_place.parking_model.inner_body.angle
        return np.array(
            [
                car_pos[0],
                car_pos[1],
                car_angle,
                car_speed,
                pp_pos[0],
                pp_pos[1],
                pp_angle,
            ]
        )

    def is_done(self):
        return self.core.scene.car_m.health <= 0 or self.core.scene.car_m.is_car_parked

    def action(self, action):
        controller = IOController()
        controller.keyboard = {
            arcade.key.LEFT: action == 0,
            arcade.key.RIGHT: action == 1,
            arcade.key.UP: action == 2,
            arcade.key.DOWN: action == 3,
            arcade.key.F: action == 4,
        }
        self.core.scene.update(controller, 1 / 60)
        self.time *= 1.01

    def evaluate(self):
        car_pos = self.core.scene.car_m.car_model.body.position
        car_angle = self.core.scene.car_m.car_model.body.angle
        # car_speed = self.core.scene.car_m.car_model.body.velocity.get_length_sqrd() ** 0.5
        pp_pos = self.core.scene.parking_place.parking_model.inner_body.position
        pp_angle = self.core.scene.parking_place.parking_model.inner_body.angle
        dst = (car_pos[0] - pp_pos[0]) ** 2 + (car_pos[1] - pp_pos[1]) ** 2
        # print(1 / (abs(car_angle - pp_angle) + 0.01), 1 / (dst + 0.01), self.time / 100, self.core.scene.car_m.health)
        return 1 / (dst + 0.01) + 1 / (abs(car_angle - pp_angle) + 0.01)
