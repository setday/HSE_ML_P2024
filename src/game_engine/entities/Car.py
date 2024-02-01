from math import radians, degrees

from src.game_engine.physics.models.CarPhysicsModel import CarPhysicsModel
from src.render.sprites.BasicSprite import BasicSprite


class Car:
    def __init__(self, render_group, space):
        self.car_view = BasicSprite("assets/car_2.png", (300, 300), render_group)
        self.car_model = CarPhysicsModel((300, 300))

        self.space = space
        self.render_group = render_group

        self.space.add(self.car_model.body, self.car_model.shape)
        # self.screen.add_drawable(self.car_view)

    def apply_friction(self):
        self.car_model.apply_friction(1.001)

    def turn_left(self, hold_brake=False):
        self.car_model.turn_left(-radians(0.1), hold_brake)

    def turn_right(self, hold_brake=False):
        self.car_model.turn_left(radians(0.1), hold_brake)

    def accelerate(self):
        self.car_model.accelerate(3)

    def brake(self):
        self.car_model.accelerate(-3)

    def hand_brake(self):
        self.car_model.brake()

    def sync(self):
        self.car_view.update_position(self.car_model.body.position)
        self.car_view.update_angle(-degrees(self.car_model.body.angle))
