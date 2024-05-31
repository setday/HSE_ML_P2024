import random

import arcade

from src.game_engine.Core import Core
from src.game_engine.controllers.Controller import (
    BrakeController,
    RandomController,
    AIController,
)
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.render.Window import IOController

from src.game_engine.scenes import GameScene


class TestCore(Core):
    def __init__(self, test_type, test_objects):
        super().__init__()
        self.type = test_type
        self.test_objects = test_objects
        self.num_obj = 0

        self.set_scene(GameScene)

    def create_object(self, obj):
        if obj == "car":
            car = ObjectFactory.create_object(
                render_group=self.scene.render_group,
                space=self.scene.space,
                object_type="car",
                position=(random.randint(-2000, 2000), random.randint(-3500, 3500)),
                car_model="red_car",
            )
            car.switch_controller(
                random.choice([RandomController(), BrakeController()])
            )
            self.scene.cars.append(car)
        elif obj == "cone":
            self.scene.traffic_cones.append(
                ObjectFactory.create_object(
                    render_group=self.scene.render_group,
                    space=self.scene.space,
                    object_type="movable_obstacle",
                    position=(random.randint(-2000, 2000), random.randint(-3500, 3500)),
                    movable_obstacle_model="cone",
                )
            )
        elif obj == "tree":
            ObjectFactory.create_object(
                self.scene.top_render_group,
                self.scene.space,
                "static_obstacle",
                (random.randint(-2000, 2000), random.randint(-3500, 3500)),
                static_obstacle_model="tree",
            )
        elif obj == "metal_pipe":
            ObjectFactory.create_object(
                self.scene.render_group,
                self.scene.space,
                "static_obstacle",
                (random.randint(-2000, 2000), random.randint(-3500, 3500)),
                90,
                static_obstacle_model="metal_pipe",
            )
        elif obj == "rubbish_line":
            ObjectFactory.create_object(
                self.scene.render_group,
                self.scene.space,
                "static_obstacle",
                (random.randint(-2000, 2000), random.randint(-3500, 3500)),
                static_obstacle_model="rubbish_line",
            )
        elif obj == "parking_place":
            ParkingPlace(
                self.scene.down_render_group,
                self.scene.space,
                (random.randint(-2000, 2000), random.randint(-3500, 3500)),
            )

    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        if io_controller.is_key_pressed(arcade.key.ESCAPE):
            arcade.exit()
            return

        for obj in self.test_objects:
            self.create_object(obj)
            self.num_obj += 1
        if not arcade.timings_enabled():
            arcade.enable_timings()
        with open(
            "data/load/" + f"{self.type}_" + "-".join(self.test_objects) + ".csv", "a"
        ) as out:
            print(f"{self.num_obj}, {arcade.get_fps()}", file=out)

        if self.type != "graphics":
            super().on_update(io_controller, delta_time)

    def on_draw(self) -> None:
        if self.type != "physics":
            super().on_draw()
