import random
from math import radians, degrees

from src.physics.models.CarPhysicsModel import CarPhysicsModel
from src.render.sprites.BasicRect import BasicRect
from src.render.sprites.BasicSprite import BasicSprite


class Car:
    def __init__(self, render_group, space, position=(300, 300), skin_id=-1):
        skins = ["assets/car_2.png", "assets/car_3.png"]  # , "assets/car_1.png"]
        if skin_id == -1:
            skin_id = random.randint(0, len(skins) - 1)
        skin = skins[skin_id]

        self.car_view = BasicSprite(skin, position)
        self.car_boundary = BasicRect(50, 100, position)
        self.car_model = CarPhysicsModel(position)

        render_group.add(self.car_view)
        render_group.add(self.car_boundary)

        self.space = space
        self.render_group = render_group

        self.car_model.shape.super = self
        self.space.add(self.car_model.body, self.car_model.shape)
        # self.screen.add_drawable(self.car_view)

        self.health = 100

    def apply_friction(self):
        self.car_model.apply_friction(1.002)

    def turn_left(self, hold_brake=False):
        self.car_model.turn_left(-radians(0.23), hold_brake)

    def turn_right(self, hold_brake=False):
        self.car_model.turn_left(radians(0.23), hold_brake)

    def accelerate(self):
        if self.health <= 0:
            return
        self.car_model.accelerate(3)

    def brake(self):
        if self.health <= 0:
            return
        self.car_model.accelerate(-3)

    def hand_brake(self):
        self.car_model.brake()

    def sync(self):
        self.car_view.update_position(self.car_model.body.position)
        self.car_view.update_angle(-degrees(self.car_model.body.angle))

        self.car_boundary.update_position(self.car_model.body.position)
        self.car_boundary.update_angle(-degrees(self.car_model.body.angle))

        self.car_boundary.update_color((0, max(self.health, 1) * 2.55, 0))

    def turn_debug_view(self, mode=True):
        pass
