import math
import random

import pymunk
from pymunk import CollisionHandler, Vec2d
from pyglet.math import Vec2 as Vector2D

import src.game_engine.scenes.game_scene.CollisionHandlers as CollisionHandlers
from src.game_engine.controllers import KeyboardController
from src.game_engine.entities.Car import Car
from src.render.Window import IOController
from src.render.particle import ParticleShow
from src.render.scene_elements import RenderGroup
from src.render.screen_elements.effect_animator import (
    EffectAnimator,
)

from src.game_engine.entities.MusicPlayer import stop_all_players
from src.render.screen_elements.ui_components.ui_sprites.NavCircle import NavCircle
from src.render.sprites import BasicSprite


class DevScene:
    def __init__(self, core_instance) -> None:
        self.core_instance = core_instance

        self.particle_show: ParticleShow = ParticleShow()

        self.score: list[int] = [0]

        ######################
        # Setup physics
        ######################

        self.space: pymunk.Space = pymunk.Space()

        h_10_10: CollisionHandler = self.space.add_collision_handler(10, 10)
        h_10_10.begin = CollisionHandlers.collision_car_with_car
        h_10_20: CollisionHandler = self.space.add_collision_handler(10, 20)
        h_10_20.begin = CollisionHandlers.collision_car_with_obstacle
        h_10_30: CollisionHandler = self.space.add_collision_handler(10, 30)
        h_10_30.begin = CollisionHandlers.collision_car_with_obstacle

        h_10_10.data["score"] = h_10_20.data["score"] = h_10_30.data["score"] = (
            self.score
        )
        h_10_10.data["debris_emitter"] = h_10_20.data["debris_emitter"] = h_10_30.data[
            "debris_emitter"
        ] = self.particle_show

        base_handler: CollisionHandler = self.space.add_collision_handler(10, 40)
        base_handler.begin = CollisionHandlers.collision_car_with_base_parking_place
        base_handler.separate = (
            CollisionHandlers.end_collision_car_with_base_parking_place
        )
        dead_handler: CollisionHandler = self.space.add_collision_handler(10, 41)
        dead_handler.begin = CollisionHandlers.collision_car_with_dead_parking_place
        dead_handler.separate = (
            CollisionHandlers.end_collision_car_with_dead_parking_place
        )

        for i in range(0, 40):
            if i == 10:
                continue
            self.space.add_collision_handler(i, 40).begin = (
                CollisionHandlers.skip_collision
            )
            self.space.add_collision_handler(i, 41).begin = (
                CollisionHandlers.skip_collision
            )

        ######################
        # Setup scene if needed
        ######################
        self.down_render_group: RenderGroup = RenderGroup()
        self.render_group: RenderGroup = RenderGroup()
        self.top_render_group: RenderGroup = RenderGroup()

        self.car_m = Car(self.render_group, self.space, Vec2d(100, 100), 0, -1, True)
        self.car_m.switch_controller(KeyboardController())
        self.cars = []
        self.traffic_cones = []
        self.parking_place = None

        h_10_10.data["sound_maker"] = h_10_20.data["sound_maker"] = h_10_30.data[
            "sound_maker"
        ] = lambda pos: 1.0

        ######################
        # Screen Elements
        ######################

        self.screen_group: RenderGroup = RenderGroup()

        ######################
        # Effects
        ######################

        self.effect_animator = EffectAnimator()

        self.upper_effect_animator = EffectAnimator()

        self.is_destroyed = False

        self.background = BasicSprite("assets/pic/map/Map.jpg")
        self.down_render_group.add(self.background)

        self.target = BasicSprite("assets/pic/extra/tyre_trail.png")
        self.render_group.add(self.target)

        self.nc = NavCircle()
        self.target_pos = Vector2D(100, 100)
        self.nc.add_target(self.car_m.car_view)

        self.poltergeist = BasicSprite("assets/pic/extra/tyre_trail.png")
        self.render_group.add(self.poltergeist)

        self.poltergeist_arr = self.nc.add_target(self.poltergeist.position)

        self.render_group.add(self.nc.sprite_list)

        self.time = 0
        self.prev_time = 0

    def do_destroy(self):
        self.core_instance = None

        self.space = None

        self.down_render_group = None
        self.render_group = None
        self.top_render_group = None
        self.screen_group = None

        self.car_m = None
        self.cars = None
        self.traffic_cones = None
        self.parking_place = None

        self.effect_animator = None
        self.upper_effect_animator = None

        self.background = None

        self.is_destroyed = True

        stop_all_players()

    def update(self, io_controller: IOController, delta_time: float) -> None:
        if self.is_destroyed:
            raise Exception("Scene is destroyed")

        self.time += delta_time
        self.target.x = self.target_pos.x = math.cos(self.time) * (self.time * 100)
        self.target.y = self.target_pos.y = math.sin(self.time) * (self.time * 100)

        delta_time = min(delta_time, 0.1)

        if (self.time - self.prev_time) > 0.03:
            self.poltergeist.x = random.randint(-300, 300)
            self.poltergeist.y = random.randint(-300, 300)

            self.poltergeist_arr.kill()
            self.poltergeist_arr = self.nc.add_target(
                self.poltergeist,
                random.choice(["enemy", "ally", "unknown", "parking_place"]),
            )

            self.prev_time = self.time

        self.effect_animator.update(delta_time)

        if self.is_destroyed:
            return

        self.update_env(io_controller, delta_time)
        self.update_screen()

        self.nc.update(delta_time)

    def update_env(self, io_controller: IOController, delta_time: float) -> None:
        keys: dict = io_controller.keyboard

        self.car_m.controlling(keys, [])
        self.car_m.apply_friction()
        self.car_m.sync()

        self.space.step(delta_time * 16)

        for car in self.cars:
            car.apply_friction()
            car.sync()

    def update_screen(self):
        ######################
        # Screen Elements Update
        ######################

        pass

    def draw(self) -> None:
        self.draw_env()
        self.draw_screen_elements()
        self.draw_effects()

    def draw_env(self):
        ######################
        # Environment Draw
        ######################

        self.render_group.camera.use()
        self.down_render_group.draw()
        for car in self.cars:
            for emitter in car.tyre_emitters:
                emitter.draw()
        self.render_group.draw()
        self.top_render_group.draw()

    def draw_screen_elements(self):
        ######################
        # Screen Elements Draw
        ######################

        self.screen_group.camera.use()
        self.screen_group.draw()

    def draw_effects(self):
        ######################
        # Shaders Draw
        ######################

        pass
