import random
from math import radians, degrees

import arcade
import numpy as np
from pymunk import Vec2d, Space

from src.physics.models.CarPhysicsModel import CarPhysicsModel
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite

import src.render.particle.ParticleShow as ParticleShow


class Car:
    def __init__(
            self,
            render_group: RenderGroup,
            space: Space,
            position: Vec2d | tuple[float, float] = (300, 300),
            angle: float = 0,
            skin_id: int = -1,
    ) -> None:
        skins: list[str] = [
            "assets/pic/cars/car_2.png",
            "assets/pic/cars/car_3.png",
            "assets/pic/cars/car_1.png",
        ]
        if skin_id == -1:
            skin_id = random.randint(0, len(skins) - 1)
        skin = skins[skin_id % len(skins)]

        x, y = position

        self.car_view: BasicSprite = BasicSprite(skin, position)
        self.car_model: CarPhysicsModel = CarPhysicsModel(
            (x, y), self.car_view.get_hit_box()
        )

        self.car_model.body.angle = angle

        self.space: Space = space
        self.render_group: RenderGroup = render_group
        self.render_group.add(self.car_view)

        self.car_model.shape.super = self

        self.space.add(self.car_model.body, self.car_model.shape)

        self.health: int = 100

        self.tyre_emitters: list[arcade.emitter] = [
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
            )
            for center in CarPhysicsModel.wheels_offset
        ]
        self.tyre_state: float = 0

        self.is_hand_braking: bool = False

        self.controller = None

        self.dead_zones_intersect: float = 0
        self.inside_parking_place: float = 0
        self.is_car_parked: bool = False

        self.hooks: dict[str, callable] = {
            "dead_hook": None,
            "parked_hook": None,
            "unparked_hook": None,
        }

        self.sync()

    def select(self) -> None:
        self.car_view.kill()
        self.car_view = BasicSprite("assets/pic/cars/car_3.png", (0, 0))
        self.render_group.add(self.car_view)
        self.sync()

    def deselect(self) -> None:
        self.car_view.kill()
        self.car_view = BasicSprite("assets/pic/cars/car_2.png", (0, 0))
        self.render_group.add(self.car_view)
        self.sync()

    def controlling(self, keys: dict, observation: list[float] | np.ndarray = None) -> None:
        self.controller.handle_input(keys, observation)

    def switch_controller(self, controller) -> None:
        self.controller = controller
        controller.connect_car(self)

    def apply_friction(self) -> None:
        self.car_model.apply_friction()

    def turn_left(self, hold_brake: bool = False) -> None:
        self.car_model.turn_left(-radians(1), hold_brake)

    def turn_right(self, hold_brake: bool = False) -> None:
        self.car_model.turn_left(radians(1), hold_brake)

    def forward_accelerate(self) -> None:
        if self.health <= 0:
            return
        self.car_model.accelerate(4)

    def backward_acceleration(self) -> None:
        if self.health <= 0:
            return
        self.car_model.accelerate(-4)

    def hand_brake(self) -> None:
        self.car_model.brake()
        self.is_hand_braking = True

    def _stop_tyring(self) -> None:
        if self.tyre_state == 0:
            return

        for emitter in self.tyre_emitters:
            emitter.rate_factory = arcade.EmitterIntervalWithTime(999999999, 999999999)
        self.tyre_state = 0

    def _start_tyring(self) -> None:
        if self.tyre_state == 1 or self.health <= 0 or not ParticleShow.particles_on:
            return

        for emitter in self.tyre_emitters:
            emitter.rate_factory = arcade.EmitterIntervalWithTime(0.03, 999999999)
        self.tyre_state = 1

    def sync(self) -> None:
        d_angle = degrees(self.car_model.body.angle)

        self.car_view.update_position(self.car_model.body.position)
        self.car_view.update_angle(d_angle)

        if self.hooks["parked_hook"] or self.hooks["unparked_hook"]:
            parked_state = (
                    self.car_model.body.velocity.get_length_sqrd() <= 0.2
                    and self.inside_parking_place
                    and self.dead_zones_intersect == 0
            )
            if parked_state != self.is_car_parked:
                self.is_car_parked = parked_state
                if self.hooks["parked_hook"] and self.is_car_parked:
                    self.hooks["parked_hook"](self)
                if self.hooks["unparked_hook"] and not self.is_car_parked:
                    self.hooks["unparked_hook"](self)

        if self.tyre_state != 0 and (
                not self.is_hand_braking
                or self.car_model.body.velocity.get_length_sqrd() < 10
        ):
            self._stop_tyring()
        if (
                self.tyre_state != 1
                and self.is_hand_braking
                and self.car_model.body.velocity.get_length_sqrd() > 10
        ):
            self._start_tyring()

        self.is_hand_braking = False

        if self.tyre_state == 0:
            return

        fwd: Vec2d = Vec2d(1, 0).rotated(self.car_model.body.angle)
        lft: Vec2d = Vec2d(0, 1).rotated(self.car_model.body.angle)

        for i in range(4):
            offset = (
                    fwd * CarPhysicsModel.wheels_offset[i][0]
                    + lft * CarPhysicsModel.wheels_offset[i][1]
                    - self.car_model.body.position
            )

            self.tyre_emitters[i].center_x = -offset.x
            self.tyre_emitters[i].center_y = offset.y

            self.tyre_emitters[i].particle_factory = (
                lambda emitter: arcade.FadeParticle(
                    filename_or_texture="assets/pic/extra/tyre_trail.png",
                    change_xy=(0, 0),
                    lifetime=1,
                    scale=1,
                    angle=90 - d_angle,
                )
            )

    def change_health(self, delta: float) -> None:
        if self.health <= 0 and delta <= 0:
            return
        if self.health >= 100 and delta >= 0:
            return

        self.health += delta
        self.health = min(max(self.health, 0), 100)
        # self.sync()

        if self.hooks["dead_hook"] and self.health <= 0:
            self.hooks["dead_hook"](self)

    def set_hook(self, hook_name: str, hook: callable):
        self.hooks[hook_name] = hook
        return self
