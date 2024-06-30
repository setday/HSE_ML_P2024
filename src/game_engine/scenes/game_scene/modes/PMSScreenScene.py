import random

import arcade
import numpy as np
from pyglet.math import Vec2 as Vector2D  # type: ignore[import-untyped]

from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.scenes.game_scene.GameSceneCore import GameSceneCore
from src.render.Window import IOController
from src.render.sprites.BasicSprite import BasicSprite


class PMSScreenScene(GameSceneCore):
    def __init__(self, core_instance):
        super().__init__(core_instance, False)

        self.background = BasicSprite("assets/pic/extra/concreate.png", Vector2D(0, 0))
        self.background.update_scale(4)
        self.down_render_group.add(self.background)

        self.car_m = ObjectFactory.create_object(
            render_group=self.render_group,
            space=self.space,
            object_type="car",
            position=(0, 0),
            car_model="blue_car",
            is_main_car=True,
        )

        self.cars = []
        for i in range(8):
            angle = np.pi / 4 * i + random.uniform(-0.1, 0.1)
            car_range = random.randint(290, 310)
            car = ObjectFactory.create_object(
                render_group=self.render_group,
                space=self.space,
                object_type="car",
                position=(car_range * np.cos(angle), car_range * np.sin(angle)),
                angle=angle / np.pi * 180 - 90 + random.uniform(-3, 3),
                car_model="red_car",
            )
            self.cars.append(car)

        # setup_scene(self, "assets/maps/ParkMe.json")

        ######################
        # Screen Elements
        ######################

        self.pause = False

    def update(self, io_controller: IOController, delta_time: float) -> None:
        if io_controller.is_key_clicked(arcade.key.P):
            self.pause = not self.pause

        if self.pause:
            return

        for car in self.cars:
            if car.car_model.body.position.length > 200:
                car.forward_accelerate()
            else:
                car.hand_brake()

        super().update(io_controller, delta_time)

    def draw_screen_elements(self):
        super().draw_screen_elements()
