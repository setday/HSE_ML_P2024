import arcade
from src.game_engine.physics.CarPhysicsModel import CarPhysicsModel
from math import radians, degrees


class Car(arcade.Sprite):
    def __init__(self, space, image="../assets/car_2.png", position=(300, 300)):
        super().__init__(image)
        self.car_model = CarPhysicsModel(position)
        self.space = space

    def apply_friction(self):
        self.car_model.apply_friction(1.002)

    def turn_left(self, hold_brake=False):
        self.car_model.turn_left(-radians(0.1), hold_brake)

    def turn_right(self, hold_brake=False):
        self.car_model.turn_left(radians(0.1), hold_brake)

    def accelerate(self):
        self.car_model.accelerate(8)

    def brake(self):
        self.car_model.accelerate(-8)

    def hand_brake(self):
        self.car_model.brake()

    def sync(self):
        self.set_position(self.car_model.body.position[0], self.car_model.body.position[1])
        self.angle = -degrees(self.car_model.body.angle)
