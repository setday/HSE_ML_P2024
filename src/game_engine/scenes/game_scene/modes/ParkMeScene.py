import numpy as np
from pyglet.math import Vec2 as Vector2D

from src.game_engine.scenes.game_scene.GameSceneCore import GameSceneCore
from src.game_engine.scenes.game_scene.SceneSetup import setup_scene
from src.render.Window import IOController
from src.render.screen_elements.Indicator import Indicator
from src.render.screen_elements.ScoreDisplay import ScoreDisplay


class ParkMeScene(GameSceneCore):
    def __init__(self, core_instance):
        super().__init__(core_instance, False)

        setup_scene(self, "assets/maps/ParkWithEnemies.json")

        self.car_m.set_hook("parked_hook", lambda _: self.do_victory())

        ######################
        # Screen Elements
        ######################

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

    def update(self, io_controller: IOController, delta_time: float) -> None:
        super().update(io_controller, delta_time)
        if self.car_m.is_car_parked and not self.is_end_state:
            self.do_victory()
        if self.car_m.health <= 0 and not self.is_end_state:
            self.do_lose()

    def update_env(self, io_controller: IOController, delta_time: float) -> None:
        keys: dict = io_controller.keyboard

        for car in self.cars:
            if car == self.car_m:
                continue
            car.controlling(
                keys,
                np.array(
                    [
                        car.car_model.body.position[0]
                        - self.parking_place.parking_model.inner_body.position[0],
                        car.car_model.body.position[1]
                        - self.parking_place.parking_model.inner_body.position[1],
                        abs(
                            car.car_model.body.angle
                            - self.parking_place.parking_model.inner_body.angle
                            + 90
                        )
                        % 180,
                        car.car_model.body.velocity.get_length_sqrd() ** 0.5,
                    ]
                ),
            )

        super().update_env(io_controller, delta_time)

    def update_screen(self):
        super().update_screen()
        self.indicator.update_bar()
        self.score_board.update_score(self.score[0])

    def draw_screen_elements(self):
        super().draw_screen_elements()
        self.score_board.draw()
