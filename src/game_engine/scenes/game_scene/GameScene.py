import random

import arcade.key
import numpy as np
import pymunk
from arcade.experimental import Shadertoy
from pyglet.math import Vec2 as Vector2D
from pymunk import CollisionHandler

from src.game_engine.controllers import RandomController, AIController, BrakeController
import src.game_engine.scenes.game_scene.CollisionHandlers as CollisionHandlers
from src.game_engine.entities.MusicPlayer import MusicPlayer
from src.game_engine.entities.ParkingPlace import ParkingPlace
from .SceneSetup import setup_scene
from ..layouts import EscapeMenuLayout
from src.game_engine.scenes.layouts.SettingLayout import get_sound_level
from src.render.scene_elements import RenderGroup
from src.render.Window import IOController
from src.render.particle import ParticleShow
from src.render.screen_elements.effect_animator import (
    EffectAnimator,
    FadeEffect,
    TextPrinter
)
from src.render.screen_elements.ui_components import (
    Indicator,
    ScoreDisplay
)


class GameScene:
    def __init__(self, core_instance, train: bool = False) -> None:
        self.core_instance = core_instance

        self.down_render_group: RenderGroup = RenderGroup()
        self.render_group: RenderGroup = RenderGroup()
        self.top_render_group: RenderGroup = RenderGroup()
        self.particle_show: ParticleShow = ParticleShow()

        self.score: list[int] = [10000]
        self.train: bool = train
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
        # Setup game objects
        ######################

        self.car_m = None
        self.cars = []
        self.traffic_cones = []

        setup_scene(self, "assets/maps/ParkWithEnemies.json")
        self.parking_place = ParkingPlace(
            self.down_render_group,
            self.space,
            position=((random.randint(-500, 500), random.randint(-500, 500))),
            angle=random.randint(0, 360),
        )
        controllers = [  # noqa: F841
            {"type": "sklearn", "path": "models_bin/CEM.pkl"},
            {"type": "pytorch", "path": "models_bin/torch.pt"},
            {"type": "stable_baselines", "policy": "DQN", "path": "models_bin/DQN"},
            {"type": "stable_baselines", "policy": "A2C", "path": "models_bin/A2C"},
            {"type": "stable_baselines", "policy": "PPO", "path": "models_bin/PPO"},
        ]
        for car in self.cars[1:]:
            car.switch_controller(
                random.choice(
                    [
                        RandomController(),
                        # Controller.AIController(random.choice(controllers)),
                        BrakeController(),
                    ]
                )
            )

        ######################
        # Screen Elements
        ######################

        self.screen_group: RenderGroup = RenderGroup()
        camera_offset: Vector2D = self.screen_group.camera.get_position(1, 1)

        self.indicator: Indicator = Indicator(
            owner=self.car_m, position=camera_offset - Vector2D(200, 100)
        )
        self.screen_group.add(self.indicator.sprite_list)

        self.score_board: ScoreDisplay = ScoreDisplay(
            score=self.score[0],
            position=camera_offset - Vector2D(200, 170),
            color=(255, 220, 40),
            font_path="assets/fnt/ka1.ttf",
            font_name="Karmatic Arcade",
        )
        self.screen_group.add(self.score_board.sprite_list)

        ######################
        # Escape Layout
        ######################

        self.escape_layout = EscapeMenuLayout(
            close_callback=lambda _: self.switch_escape_layout(),
            home_callback=lambda _: self.go_home(),
        )
        self.is_escape_layout_open = False
        self.is_escape_layout_renders = False

        ######################
        # Shaders Setup
        ######################

        # file = open("src/shaders/toy/fractal_pyramid.glsl")
        file = open("src/shaders/vignette/vignette.glsl")
        shader_sourcecode = file.read()
        self.shader_vin = Shadertoy((1920, 1080), shader_sourcecode)

        self.tick = 0

        ######################
        # Effects
        ######################

        self.effect_animator = EffectAnimator()
        self.effect_animator.add_effect(
            FadeEffect(1, 0, None, (255, 255, 255, 255), False)
        )

        self.upper_effect_animator = EffectAnimator()

        self.is_end_state = False

    def init_music_player(self, window):
        self.music_player = MusicPlayer(window, 1.0 * get_sound_level())

    def update(self, io_controller: IOController, delta_time: float) -> None:
        self.effect_animator.update(delta_time)

        if self.is_escape_layout_renders:
            self.escape_layout.update(io_controller, delta_time)

            self.upper_effect_animator.update(delta_time)
        else:
            if io_controller.is_key_clicked(arcade.key.ESCAPE):
                self.switch_escape_layout()
                return

        if self.is_escape_layout_open:
            return

        if io_controller.is_key_clicked(arcade.key.F7):
            self.car_m.change_health(1000)

        self.update_env(io_controller, delta_time)
        self.update_screen()

    def update_env(self, io_controller: IOController, delta_time: float) -> None:
        keys: dict = io_controller.keyboard

        if isinstance(self.car_m.controller, AIController):
            self.car_m.controlling(
                keys,
                np.array(
                    [
                        self.car_m.car_model.body.position[0]
                        - self.parking_place.parking_model.inner_body.position[0],
                        self.car_m.car_model.body.position[1]
                        - self.parking_place.parking_model.inner_body.position[1],
                        abs(
                            self.car_m.car_model.body.angle
                            - self.parking_place.parking_model.inner_body.angle
                        )
                        % 180,
                        self.car_m.car_model.body.velocity.get_length_sqrd() ** 0.5,
                    ]
                ),
            )
        else:
            self.car_m.controlling(keys)

        for car in self.cars:
            if car == self.car_m:
                continue
            if isinstance(car.controller, AIController):
                car.controlling(
                    keys,
                    np.array(
                        [
                            self.car_m.car_model.body.position[0]
                            - self.parking_place.parking_model.inner_body.position[0],
                            self.car_m.car_model.body.position[1]
                            - self.parking_place.parking_model.inner_body.position[1],
                            abs(
                                self.car_m.car_model.body.angle
                                - self.parking_place.parking_model.inner_body.angle
                            )
                            % 180,
                            self.car_m.car_model.body.velocity.get_length_sqrd() ** 0.5,
                            # self.parking_place.parking_model.inner_body.angle,
                        ]
                    ),
                )
            else:
                car.controlling(keys)

        self.space.step(delta_time * 16)

        for car in self.cars:
            car.apply_friction()
            car.sync()
            for emitter in car.tyre_emitters:
                emitter.update()

        for cone in self.traffic_cones:
            cone.apply_friction()
            cone.sync()

        zoom_factor: float = (
                1 + self.car_m.car_model.body.velocity.get_length_sqrd() / 10000
        )

        self.render_group.camera.set_zoom(zoom_factor)
        self.screen_group.camera.set_zoom(zoom_factor)

        self.particle_show.update()

    def update_screen(self):
        ######################
        # Screen Elements Update
        ######################

        self.indicator.update_bar()
        self.score_board.update_score(self.score[0])

        if self.car_m.health <= 0 and not self.is_end_state:
            self.is_end_state = True

            self.effect_animator.add_effect(
                FadeEffect(1, 0, None, (0, 0, 0, 200), True, True)
            )
            self.effect_animator.add_effect(
                TextPrinter(2.3, 0, None, "You   LOSE", True, None, True)
            )
            self.effect_animator.add_effect(
                FadeEffect(
                    2,
                    2,
                    lambda: self.core_instance.set_scene(None),
                    (255, 255, 255, 255),
                    True,
                    True,
                )
            )

    def draw(self) -> None:
        self.render_group.camera.use()
        self.down_render_group.draw()
        for car in self.cars:
            for emitter in car.tyre_emitters:
                emitter.draw()
        self.render_group.draw()
        self.particle_show.draw()
        self.top_render_group.draw()

        ######################
        # Screen Elements Draw
        ######################

        self.screen_group.camera.use()
        self.screen_group.draw()
        self.score_board.draw()
        self.music_player.draw()

        ######################
        # Shaders Draw
        ######################

        self.tick += 1

        self.shader_vin.render(time=self.tick / 125, time_delta=self.car_m.health)

        self.effect_animator.draw()

        if self.is_escape_layout_renders:
            self.escape_layout.draw()

            self.upper_effect_animator.draw()

    def switch_escape_layout(self):
        if self.is_end_state:
            return

        self.is_escape_layout_open = not self.is_escape_layout_open

        if self.is_escape_layout_open:
            self.effect_animator.add_effect(
                FadeEffect(0.5, 0, None, (0, 0, 0, 100), True, True)
            )
            self.is_escape_layout_renders = True
            self.escape_layout.show()
        else:
            self.effect_animator.clear_effects()
            self.effect_animator.clear_post_effects()
            self.effect_animator.add_effect(
                FadeEffect(
                    0.5,
                    0,
                    lambda: self.show_escape_layout(False),
                    (0, 0, 0, 100),
                    False,
                )
            )
            self.escape_layout.hide()

    def go_home(self):
        self.is_end_state = True
        self.upper_effect_animator.add_effect(
            FadeEffect(
                1,
                0,
                lambda: [self.music_player.pause(), self.core_instance.set_scene(None)],
                (255, 255, 255, 255),
                True,
                True,
            )
        )

    def show_escape_layout(self, show: bool):
        self.is_escape_layout_renders = show
