import random
from math import radians, degrees

import arcade
from pymunk import Vec2d

from src.physics.models.CarPhysicsModel import CarPhysicsModel
from src.render.sprites.BasicSprite import BasicSprite


class Car:
    def __init__(self, render_group, space, position=(300, 300), angle=0, skin_id=-1):
        skins = ["assets/pic/cars/car_2.png", "assets/pic/cars/car_3.png", "assets/pic/cars/car_1.png"]
        if skin_id == -1:
            skin_id = random.randint(0, len(skins) - 1)
        skin = skins[skin_id % len(skins)]

        x, y = position

        self.car_view = BasicSprite(skin, position)
        self.car_model = CarPhysicsModel((x, y), self.car_view.get_hit_box())

        self.car_model.body.angle = angle

        render_group.add(self.car_view)

        self.space = space
        self.render_group = render_group

        self.car_model.shape.super = self

        self.space.add(self.car_model.body, self.car_model.shape)

        self.health = 100

        self.tyre_emitters = [
            arcade.make_interval_emitter(
                center_xy=center,
                filenames_and_textures=[
                    "assets/pic/tyre_trail.png",
                ],
                emit_interval=999999999,
                emit_duration=999999999,
                particle_speed=0,
                particle_lifetime_max=1,
                particle_lifetime_min=1,
                fade_particles=True,
            ) for center in CarPhysicsModel.wheels_offset
        ]
        self.tyre_state = 0

        self.is_hand_braking = False

        self.sync()

        self.controller = None

    def controlling(self, keys):
        self.controller.handle_input(keys)

    def switch_controller(self, controller):
        self.controller = controller
        controller.connect_car(self)

    def apply_friction(self):
        self.car_model.apply_friction()

    def turn_left(self, hold_brake=False):
        self.car_model.turn_left(-radians(1), hold_brake)

    def turn_right(self, hold_brake=False):
        self.car_model.turn_left(radians(1), hold_brake)

    def forward_accelerate(self):
        if self.health <= 0:
            return
        self.car_model.accelerate(4)

    def backward_acceleration(self):
        if self.health <= 0:
            return
        self.car_model.accelerate(-4)

    def hand_brake(self):
        self.car_model.brake()
        self.is_hand_braking = True

    def _stop_tyring(self):
        if self.tyre_state == 0:
            return

        for emitter in self.tyre_emitters:
            emitter.rate_factory = arcade.EmitterIntervalWithTime(999999999, 999999999)
        self.tyre_state = 0

    def _start_tyring(self):
        if self.tyre_state == 1:
            return

        for emitter in self.tyre_emitters:
            emitter.rate_factory = arcade.EmitterIntervalWithTime(0.03, 999999999)
        self.tyre_state = 1

    def sync(self):
        d_angle = degrees(self.car_model.body.angle)

        self.car_view.update_position(self.car_model.body.position)
        self.car_view.update_angle(d_angle)

        if self.tyre_state != 0 and (not self.is_hand_braking or self.car_model.body.velocity.get_length_sqrd() < 10):
            self._stop_tyring()
        if self.tyre_state != 1 and self.is_hand_braking and self.car_model.body.velocity.get_length_sqrd() > 10:
            self._start_tyring()

        self.is_hand_braking = False

        if self.tyre_state == 0:
            return

        fwd = Vec2d(1, 0).rotated(self.car_model.body.angle)
        lft = Vec2d(0, 1).rotated(self.car_model.body.angle)

        for i in range(4):
            offset = fwd * CarPhysicsModel.wheels_offset[i][0] + lft * CarPhysicsModel.wheels_offset[i][1] - \
                     self.car_model.body.position

            self.tyre_emitters[i].center_x = -offset.x
            self.tyre_emitters[i].center_y = offset.y

            self.tyre_emitters[i].particle_factory = lambda emitter: arcade.FadeParticle(
                filename_or_texture='assets/pic/extra/tyre_trail.png',
                change_xy=(0, 0),
                lifetime=1,
                scale=1,
                angle=90 - d_angle,
            )
