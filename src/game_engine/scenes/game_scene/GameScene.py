import time

import arcade.key
import pymunk
from pyglet.math import Vec2 as Vector2D

from src.game_engine.controllers.Controller import *
from src.game_engine.entities.Car import Car
from src.render.screen_elements.ScoreDisplay import ScoreDisplay
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
from src.game_engine.scenes.game_scene.CollisionHandlers import collision_car_with_car, collision_car_with_obstacle
from src.render.RenderGroup import RenderGroup
from src.render.particle.ParticleShow import ParticleShow
from src.render.screen_elements.Indicator import Indicator
from src.render.sprites.BasicSprite import BasicSprite


class GameScene:
    def __init__(self):
        self.down_render_group = RenderGroup()
        self.render_group = RenderGroup()
        self.top_render_group = RenderGroup()
        self.space = pymunk.Space()
        self.particle_show = ParticleShow()
        self.score: list[int] = [10000]

        h_10_10 = self.space.add_collision_handler(10, 10)
        h_10_10.begin = collision_car_with_car
        h_10_20 = self.space.add_collision_handler(10, 20)
        h_10_20.begin = collision_car_with_obstacle
        h_10_30 = self.space.add_collision_handler(10, 30)
        h_10_30.begin = collision_car_with_obstacle

        h_10_10.data["score"] = h_10_20.data["score"] = h_10_30.data["score"] = self.score
        h_10_10.data["debris_emitter"] = h_10_20.data["debris_emitter"] = \
            h_10_30.data["debris_emitter"] = self.particle_show

        self.background = BasicSprite("assets/pic/Map.jpg", Vector2D(0, 0))
        self.background.update_scale(10)

        self.down_render_group.add(self.background)

        self.car_m = Car(self.render_group, self.space, (0, -100), 0)

        self.car_m.switch_controller(KeyboardController())

        self.render_group.camera.snap_to_sprite(self.car_m.car_view)


        self.cars = [self.car_m]
        for i in range(-5, 5):
            if i == 0:
                continue
            car = Car(self.render_group, self.space, (70 * i, -100), 1)
            car.switch_controller(random.choice([RandomController(), AIController(), BrakeController()]))
            self.cars.append(car)

        self.traffic_cones = []
        for i in range(-5, 5):
            self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * i, -170)))

        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * -5 - 35, -70)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * -5 - 40, -100)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * -5 - 35, -130)))

        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * 4 + 35, -70)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * 4 + 40, -100)))
        self.traffic_cones.append(MovableObstacle(self.render_group, self.space, (70 * 4 + 35, -130)))

        for i in range(-5, 5):
            StaticObstacle(self.top_render_group, self.space, (70 * i, -10))

        ######################
        # Screen Elements
        ######################

        self.screen_group = RenderGroup()
        camera_offset = self.screen_group.camera.get_position(1, 1)

        self.indicator = Indicator(owner=self.car_m, position=camera_offset - Vector2D(200, 100))
        self.screen_group.add(self.indicator.sprite_list)

        self.score_board = ScoreDisplay(score=self.score[0], position=camera_offset - Vector2D(200, 170),
                                        color=(255, 220, 40),
                                        font_path='assets/ka1.ttf', font_name='Karmatic Arcade')
        self.screen_group.add(self.score_board.sprite_list)

    def update(self, io_controller, delta_time):
        keys = io_controller.keyboard

        if keys.get(arcade.key.F6, False):
            image = arcade.get_image()
            image.save(f"data/screenshots/{time.time()}.png")

        if keys.get(arcade.key.F7, False):
            self.car_m.health = 100

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

        zoom_factor = 1 + self.car_m.car_model.body.velocity.get_length_sqrd() / 10000

        self.render_group.camera.set_zoom(zoom_factor)

        self.particle_show.update()

        ######################
        # Screen Elements Update
        ######################

        self.screen_group.camera.set_zoom(zoom_factor)

        self.indicator.update_bar()
        self.score_board.update_score(self.score[0])

    def draw(self):
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
