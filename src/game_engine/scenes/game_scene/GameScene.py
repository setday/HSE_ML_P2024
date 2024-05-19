import time
from pymunk import CollisionHandler
from src.render.Window import IOController
import arcade.key
import pymunk
from pyglet.math import Vec2 as Vector2D
import random
from src.game_engine.controllers.Controller import (
    KeyboardController,
    BrakeController,
    RandomController,
    AIController,
)
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.ParkingPlace import ParkingPlace
import src.game_engine.scenes.game_scene.CollisionHandlers as CollisionHandlers
from src.render.RenderGroup import RenderGroup
from src.render.particle.ParticleShow import ParticleShow
from src.render.screen_elements.Indicator import Indicator
from src.render.screen_elements.ScoreDisplay import ScoreDisplay
from src.render.sprites.BasicSprite import BasicSprite
from src.game_engine.entities.Car import Car
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle


class GameScene:
    def __init__(self) -> None:
        self.down_render_group: RenderGroup = RenderGroup()
        self.render_group: RenderGroup = RenderGroup()
        self.top_render_group: RenderGroup = RenderGroup()
        self.particle_show: ParticleShow = ParticleShow()
        self.score: list[int] = [10000]

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

        h_10_10.data["score"] = h_10_20.data["score"] = h_10_30.data[
            "score"
        ] = self.score
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
            self.space.add_collision_handler(
                i, 40
            ).begin = CollisionHandlers.skip_collision
            self.space.add_collision_handler(
                i, 41
            ).begin = CollisionHandlers.skip_collision

        ######################
        # Setup game objects
        ######################

        self.background: BasicSprite = BasicSprite("assets/pic/map/Map.jpg", (0, 0))
        self.background.update_scale(10)

        self.down_render_group.add(self.background)

        self.car_m: Car = ObjectFactory.create_object(
            render_group=self.render_group,
            space=self.space,
            object_type="car",
            position=(0, -100),
            car_model="blue_car",
        )

        self.car_m.switch_controller(KeyboardController())
        # self.car_m.set_hook("dead_hook", lambda _: print("You dead"))
        # self.car_m.set_hook("parked_hook", lambda _: print("You win"))
        # self.car_m.set_hook("unparked_hook", lambda _: print("You out"))

        self.render_group.camera.snap_to_sprite(self.car_m.car_view)

        self.cars: list[Car] = [self.car_m]
        for i in range(-5, 5):
            if i == 0:
                continue
            car = ObjectFactory.create_object(
                render_group=self.render_group,
                space=self.space,
                object_type="car",
                position=(70 * i, -100),
                car_model="red_car",
            )
            car.switch_controller(
                random.choice([RandomController(), AIController(), BrakeController()])
            )
            self.cars.append(car)

        self.traffic_cones: list[MovableObstacle] = []
        for i in range(-5, 5):
            self.traffic_cones.append(
                ObjectFactory.create_object(
                    render_group=self.render_group,
                    space=self.space,
                    object_type="movable_obstacle",
                    position=(70 * i, -170),
                    movable_obstacle_model="cone",
                )
            )

        self.traffic_cones.append(
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "movable_obstacle",
                (70 * -5 - 35, -70),
                movable_obstacle_model="cone",
            )
        )
        self.traffic_cones.append(
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "movable_obstacle",
                (70 * -5 - 40, -100),
                movable_obstacle_model="cone",
            )
        )
        self.traffic_cones.append(
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "movable_obstacle",
                (70 * -5 - 35, -130),
                movable_obstacle_model="cone",
            )
        )

        self.traffic_cones.append(
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "movable_obstacle",
                (70 * 4 + 35, -70),
                movable_obstacle_model="cone",
            )
        )
        self.traffic_cones.append(
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "movable_obstacle",
                (70 * 4 + 40, -100),
                movable_obstacle_model="cone",
            )
        )
        self.traffic_cones.append(
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "movable_obstacle",
                (70 * 4 + 35, -130),
                movable_obstacle_model="cone",
            )
        )

        for i in range(-5, 5):
            ObjectFactory.create_object(
                self.top_render_group,
                self.space,
                "static_obstacle",
                (70 * i, -10),
                static_obstacle_model="tree",
            )

        ###
        # Parking lots
        ###

        for i in range(-5, 5):
            ParkingPlace(self.down_render_group, self.space, (70 * i, -100))
        for i in range(-5, 4):
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "static_obstacle",
                (70 * i + 35, -100),
                90,
                static_obstacle_model="metal_pipe",
            )
        for i in range(-5, 5):
            ObjectFactory.create_object(
                self.render_group,
                self.space,
                "static_obstacle",
                (70 * i, -45),
                static_obstacle_model="rubbish_line",
            )

        ###
        # Barriers
        ###

        ObjectFactory.create_object(
            self.render_group,
            self.space,
            "static_obstacle",
            (0, 1000),
            static_obstacle_model="x_barrier",
        )
        ObjectFactory.create_object(
            self.render_group,
            self.space,
            "static_obstacle",
            (0, -2000),
            static_obstacle_model="x_barrier",
        )
        ObjectFactory.create_object(
            self.render_group,
            self.space,
            "static_obstacle",
            (3500, 0),
            static_obstacle_model="y_barrier",
        )
        ObjectFactory.create_object(
            self.render_group,
            self.space,
            "static_obstacle",
            (-3500, 0),
            static_obstacle_model="y_barrier",
        )

        ParkingPlace(self.down_render_group, self.space, (0, -300), angle=0.4)

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

    def update(self, io_controller: IOController, delta_time: float) -> None:
        keys: dict = io_controller.keyboard

        if keys.get(arcade.key.F6, False):
            image = arcade.get_image()
            image.save(f"data/screenshots/{time.time()}.png")

        if keys.get(arcade.key.F7, False):
            self.car_m.change_health(1000)

        self.car_m.controlling(keys)

        for car in self.cars:
            if car == self.car_m:
                continue
            car.controlling(keys)

        delta_time *= 16

        self.space.step(delta_time)

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

        self.particle_show.update()

        ######################
        # Screen Elements Update
        ######################

        self.screen_group.camera.set_zoom(zoom_factor)

        self.indicator.update_bar()
        self.score_board.update_score(self.score[0])

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
