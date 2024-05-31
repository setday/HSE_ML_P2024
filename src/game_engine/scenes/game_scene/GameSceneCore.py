import arcade.key
import numpy as np
import pymunk
from arcade.experimental import Shadertoy
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
    TextPrinter,
)
from src.render.screen_elements.ui_components import Indicator, ScoreDisplay


class GameSceneCore:
    def __init__(self, core_instance, train: bool = False) -> None:
        self.core_instance = core_instance
        self.particle_show: ParticleShow = ParticleShow()

        self.score: list[int] = [0]
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
        # Setup scene if needed
        ######################
        self.down_render_group: RenderGroup = RenderGroup()
        self.render_group: RenderGroup = RenderGroup()
        self.top_render_group: RenderGroup = RenderGroup()

        self.car_m: Car | None = None
        self.cars: list[Car] = []
        self.traffic_cones: list[MovableObstacle] = []
        self.parking_place: ParkingPlace | None = None

        ######################
        # Screen Elements
        ######################

        self.screen_group: RenderGroup = RenderGroup()

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
        delta_time = min(delta_time, 0.1)

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

        # if io_controller.is_key_clicked(arcade.key.F7):
        #     self.car_m.change_health(1000)

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
                        self.car_m.car_model.body.velocity.length,
                    ]
                ),
            )
        else:
            self.car_m.controlling(keys)

        for car in self.cars:
            if car == self.car_m:
                continue
            if not isinstance(car.controller, AIController):
                car.controlling(keys)
                continue

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
        self.particle_show.draw()
        self.top_render_group.draw()

    def draw_screen_elements(self):
        ######################
        # Screen Elements Draw
        ######################

        self.screen_group.camera.use()
        self.screen_group.draw()
        self.score_board.draw()
        self.music_player.draw()

    def draw_effects(self):
        ######################
        # Shaders Draw
        ######################

        self.tick += 1

        if self.car_m:
            self.shader_vin.render(time=self.tick / 125, time_delta=self.car_m.health)

        self.effect_animator.draw()

        if self.is_escape_layout_renders:
            self.escape_layout.draw()

            self.upper_effect_animator.draw()

    def do_lose(self):
        self.is_end_state = True

        self.effect_animator.add_effect(
            FadeEffect(1, 0, None, (0, 0, 0, 200), True, True)
        )
        self.effect_animator.add_effect(
            TextPrinter(
                2.3,
                0,
                None,
                "You   LOSE",
                arcade.color.LIGHT_PINK,
                100,
                True,
                None,
                (0, 50),
                True,
            )
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

    def do_victory(self):
        self.is_end_state = True

        self.effect_animator.add_effect(
            FadeEffect(1, 0, None, (0, 0, 0, 200), True, True)
        )
        self.effect_animator.add_effect(
            TextPrinter(
                1.6,
                0,
                None,
                "Victory!",
                arcade.color.GOLD,
                100,
                True,
                None,
                (0, 50),
                True,
            )
        )
        self.effect_animator.add_effect(
            TextPrinter(
                3,
                2,
                None,
                f"with score: {int(self.score[0])}!",
                arcade.color.GOLD,
                32,
                True,
                None,
                (0, -50),
                True,
            )
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
