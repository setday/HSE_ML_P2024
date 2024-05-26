import time
import random

import arcade.key
import pymunk
from pyglet.math import Vec2 as Vector2D
import math

from src.game_engine.controllers.Controller import *
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.game_engine.scenes.game_scene.CollisionHandlers import *
from src.render.RenderGroup import RenderGroup
from src.render.particle.ParticleShow import ParticleShow
from src.render.screen_elements.ScoreDisplay import ScoreDisplay
from src.render.sprites.BasicSprite import BasicSprite


class LearningScene:
    def reset(self):
        self.score = 0

        self.down_render_group = RenderGroup()
        self.render_group = RenderGroup()
        self.top_render_group = RenderGroup()
        self.particle_show = ParticleShow()
        self.score: list[int] = [10000]

        self.space = pymunk.Space()

        h_10_10 = self.space.add_collision_handler(10, 10)
        h_10_10.begin = skip_collision
        h_10_20 = self.space.add_collision_handler(10, 20)
        h_10_20.begin = collision_car_with_obstacle
        h_10_30 = self.space.add_collision_handler(10, 30)
        h_10_30.begin = collision_car_with_obstacle

        h_10_10.data["score"] = h_10_20.data["score"] = h_10_30.data["score"] = self.score
        h_10_10.data["debris_emitter"] = h_10_20.data["debris_emitter"] = \
            h_10_30.data["debris_emitter"] = self.particle_show

        base_handler = self.space.add_collision_handler(10, 40)
        base_handler.begin = collision_car_with_base_parking_place
        base_handler.separate = end_collision_car_with_base_parking_place
        dead_handler = self.space.add_collision_handler(10, 41)
        dead_handler.begin = collision_car_with_dead_parking_place
        dead_handler.separate = end_collision_car_with_dead_parking_place

        for i in range(0, 40):
            if i == 10:
                continue
            self.space.add_collision_handler(i, 40).begin = skip_collision
            self.space.add_collision_handler(i, 41).begin = skip_collision


        self.background = BasicSprite("assets/pic/map/Map.jpg", (0, 0))
        self.background.update_scale(10)

        self.down_render_group.add(self.background)

        self.population_size = 100
        self.cars = []
        for i in range(self.population_size):
            angle = 2 * math.pi * random.random()
            self.cars.append(ObjectFactory.create_object(render_group=self.render_group,
                                                 space=self.space,
                                                 object_type='car',
                                                 position=(
                                                    # 600 * math.cos(2 * math.pi * i / self.population_size),
                                                    500 * math.cos(angle),
                                                    # 600 * math.sin(2 * math.pi * i / self.population_size)
                                                    500 * math.sin(angle)
                                                 ),
                                                 angle=360 * random.random(),
                                                 car_model='blue_car')
            )

        for car in self.cars:
            car.switch_controller(AIController())
            # car.set_hook("dead_hook", lambda _: print("You dead"))
            # car.set_hook("parked_hook", lambda _: print("You win"))
            # car.set_hook("unparked_hook", lambda _: print("You out"))

        self.parking_place = ParkingPlace(self.down_render_group, self.space, (0, 0), angle=math.pi/4)

        # self.render_group.camera.snap_to_sprite(self.car_m.car_view)
        self.render_group.camera.snap_to_sprite(self.parking_place.border_box)

        ######################
        # Screen Elements
        ######################

        self.screen_group = RenderGroup()
        # camera_offset = self.screen_group.camera.get_position(1, 1)

        # self.best_car_dst = [10 ** 9 for i in range(self.population_size)]

        self.ticks_elapsed = 0

    def __init__(self):
        self.reset()


    def link_models(self, models):
        for i in range(self.population_size):
            self.cars[i].controller.link_model(models[i])


    def link_genomes(self, genomes):
        self.genomes = genomes


    def set_tick_lim(self, tick_lim):
        self.tick_lim = tick_lim


    def update(self, io_controller, delta_time):
        keys = io_controller.keyboard

        for i, car in enumerate(self.cars):
            car_pos = car.car_model.body.position
            car_angle = car.car_model.body.angle
            car_speed = car.car_model.body.velocity.get_length_sqrd() ** 0.5

            pp_pos = self.parking_place.parking_model.inner_body.position
            pp_angle = self.parking_place.parking_model.inner_body.angle

            car.controlling(keys, [*car_pos, car_angle, car_speed, *pp_pos, pp_angle])

            dst = (car_pos[0] - pp_pos[0]) * (car_pos[0] - pp_pos[0]) + \
                  (car_pos[1] - pp_pos[1]) * (car_pos[1] - pp_pos[1])

            self.genomes[i][1].fitness += 1 / (abs(car_angle - pp_angle) + 10) + 1000 / (dst + 1) - 1 / (car_speed + 10)

            # self.genomes[i][1].fitness += (self.best_car_dst[i] - dst) / (self.best_car_dst[i] + dst + 0.1 ** 10)
            # self.best_car_dst[i] = max(self.best_car_dst[i], dst)

        delta_time *= 16

        self.space.step(delta_time)
        self.ticks_elapsed += delta_time
        if self.ticks_elapsed > self.tick_lim:
            arcade.close_window()

        for car in self.cars:
            car.apply_friction()
            car.sync()
            for emitter in car.tyre_emitters:
                emitter.update()

        self.particle_show.update()


    def draw(self):
        self.render_group.camera.use()
        self.down_render_group.draw()
        self.render_group.draw()
        self.particle_show.draw()
        self.top_render_group.draw()

        ######################
        # Screen Elements Draw
        ######################

        self.screen_group.camera.use()
        self.screen_group.draw()

    def get_score(self):
        return self.score
