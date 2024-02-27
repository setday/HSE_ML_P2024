import random
from math import radians, degrees

from pymunk import Vec2d

from src.physics.models.CarPhysicsModel import CarPhysicsModel
from src.render.sprites.BasicRect import BasicRect
from src.render.sprites.BasicSprite import BasicSprite


class Car:
    def __init__(self, render_group, space, position=(300, 300), skin_id=-1):
        skins = ["assets/car_2.png"]#, "assets/car_3.png"]  # , "assets/car_1.png"]
        if skin_id == -1:
            skin_id = random.randint(0, len(skins) - 1)
        skin = skins[skin_id % len(skins)]

        self.car_view = BasicSprite(skin, position)
        self.car_boundary = BasicRect(50, 100, position)
        self.car_model = CarPhysicsModel(position)

        render_group.add_sprite("cv" + random.randint(0, 100000).__str__(), self.car_view)
        render_group.add_sprite("cb" + random.randint(0, 100000).__str__(), self.car_boundary)

        self.space = space
        self.render_group = render_group

        self.car_model.shape.super = self
        self.space.add(self.car_model.body, self.car_model.shape)
        # self.screen.add_drawable(self.car_view)

        self.health = 100

    def apply_friction(self):
        self.car_model.apply_friction(1.02)

    def turn_left(self, hold_brake=False):
        self.car_model.turn_left(-radians(1), hold_brake)

    def turn_right(self, hold_brake=False):
        self.car_model.turn_left(radians(1), hold_brake)

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
        def inverse_y(pos):
            return Vec2d(pos.x, -pos.y)

        self.car_view.update_position(inverse_y(self.car_model.body.position))
        self.car_view.update_angle(-degrees(self.car_model.body.angle))

        self.car_boundary.update_position(inverse_y(self.car_model.body.position))
        self.car_boundary.update_angle(-degrees(self.car_model.body.angle))

    def turn_debug_view(self, mode=True):
        pass
