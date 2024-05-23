import arcade.key
import numpy as np

from src.game_engine.Core import Core
from src.render.Window import IOController


class Game:
    def __init__(self):
        self.core = Core(True)
        # self.time = 1
        # car_pos = self.core.scene.car_m.car_model.body.position
        # car_angle = self.core.scene.car_m.car_model.body.angle
        # car_speed = (
        #         self.core.scene.car_m.car_model.body.velocity.get_length_sqrd() ** 0.5
        # )
        # pp_pos = self.core.scene.parking_place.parking_model.inner_body.position
        # pp_angle = self.core.scene.parking_place.parking_model.inner_body.angle
        # self.state = np.array(
        #     [
        #         car_pos[0] - pp_pos[0],
        #         car_pos[1] - pp_pos[1],
        #         int(abs(car_angle - pp_angle)) % 180,
        #         car_speed,
        #     ]
        # )

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
                car_pos[0] - pp_pos[0],
                car_pos[1] - pp_pos[1],
                car_angle - pp_angle,
                car_speed,
            ]
        )

    def is_done(self):
        return self.core.scene.car_m.health <= 0 or self.core.scene.car_m.is_car_parked

    def action(self, action):
        controller = IOController()
        # 5 is left-forward
        # 6 is right-forward
        # 7 is left-back
        # 8 is right-back
        controller.keyboard = {
            arcade.key.LEFT: action == 0 or action == 5 or action == 7,
            arcade.key.RIGHT: action == 1 or action == 6 or action == 8,
            arcade.key.UP: action == 2 or action == 5 or action == 6,
            arcade.key.DOWN: action == 3 or action == 7 or action == 8,
            arcade.key.F: action == 4,
        }
        self.core.scene.update(controller, 1 / 60)
        # self.time *= 1.01

    def evaluate(self):
        car_pos = self.core.scene.car_m.car_model.body.position
        car_angle = self.core.scene.car_m.car_model.body.angle
        # car_speed = (
        #     self.core.scene.car_m.car_model.body.velocity.get_length_sqrd() ** 0.5
        # )
        pp_pos = self.core.scene.parking_place.parking_model.inner_body.position
        pp_angle = self.core.scene.parking_place.parking_model.inner_body.angle
        # delta_x = abs(self.state[0]) - abs(car_pos[0] - pp_pos[0])
        # delta_y = abs(self.state[1]) - abs(car_pos[1] - pp_pos[1])
        # delta_angle = self.state[2] - int(abs(car_angle - pp_angle)) % 180
        # self.state = np.array(
        #     [
        #         car_pos[0] - pp_pos[0],
        #         car_pos[1] - pp_pos[1],
        #         int(abs(car_angle - pp_angle)) % 180,
        #         car_speed,
        #     ]
        # )
        dst = (car_pos[0] - pp_pos[0]) ** 2 + (car_pos[1] - pp_pos[1]) ** 2
        angle = abs(car_angle - pp_angle) % 180 + 0.001
        return self.core.scene.car_m.is_car_parked * 1000000 + min(1 / dst, 1 / angle, 1e6)

