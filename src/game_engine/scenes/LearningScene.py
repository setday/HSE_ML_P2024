import random

import pymunk
import math

from src.game_engine.controllers.Controller import AIController
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.game_engine.scenes.game_scene.CollisionHandlers import (
    skip_collision,
    collision_car_with_base_parking_place,
    collision_car_with_dead_parking_place,
    end_collision_car_with_base_parking_place,
    end_collision_car_with_dead_parking_place,
)
from src.render.RenderGroup import RenderGroup
from src.render.particle.ParticleShow import ParticleShow
from src.render.sprites.BasicSprite import BasicSprite


class LearningScene:
    def __init__(self):
        self.down_render_group = RenderGroup()
        self.render_group = RenderGroup()
        self.top_render_group = RenderGroup()
        self.particle_show = ParticleShow()
        self.score: list[int] = [10000]

        self.space = pymunk.Space()

        h_10_10 = self.space.add_collision_handler(10, 10)
        h_10_10.begin = skip_collision

        base_handler = self.space.add_collision_handler(10, 40)
        base_handler.begin = collision_car_with_base_parking_place
        base_handler.separate = end_collision_car_with_base_parking_place
        dead_handler = self.space.add_collision_handler(10, 41)
        dead_handler.begin = collision_car_with_dead_parking_place
        dead_handler.separate = end_collision_car_with_dead_parking_place

        self.background = BasicSprite("assets/pic/map/Map.jpg", (0, 0))
        self.background.update_scale(10)

        self.down_render_group.add(self.background)

        self.population_size = 200
        self.cars = []
        for i in range(self.population_size):
            self.cars.append(
                ObjectFactory.create_object(
                    render_group=self.render_group,
                    space=self.space,
                    object_type="car",
                    position=(0, 0),
                    angle=0,
                    car_model="blue_car",
                )
            )

        for car in self.cars:
            car.switch_controller(AIController())

        self.parking_place = ParkingPlace(
            self.down_render_group, self.space, (0, 0), angle=0
        )

        self.render_group.camera.snap_to_sprite(self.parking_place.border_box)

        self.screen_group = RenderGroup()

        self.tick_lim = 20

        self.genomes = None
        self.state = -1
        self.ticks_elapsed = 0
        self.gen = 0

        self.reset()

    def reset(self):
        self.state = 0
        for i in range(self.population_size):
            angle = 2 * math.pi * random.random()
            self.cars[i].car_model.body.position = (
                250 * math.cos(angle),
                250 * math.sin(angle),
            )
            self.cars[i].car_model.body.angle = (
                angle - math.pi / 2
            )  # very simple task, just drive forward
        self.ticks_elapsed = 0

        self.fitnesses = [0 for i in range(self.population_size)]

    def link_models(self, models):
        for i in range(self.population_size):
            self.cars[i].controller.link_model(models[i])

    def link_genomes(self, genomes):
        self.genomes = genomes

    def update_cars_fitness(self):
        self.gen += 1
        print(f"Gen #{self.gen}", end="\r")
        for i, car in enumerate(self.cars):
            self.genomes[i][1].fitness = self.fitnesses[i]

    def update(self, io_controller, delta_time):
        if self.state == 0:
            return

        keys = io_controller.keyboard

        for i, car in enumerate(self.cars):
            car_pos = car.car_model.body.position
            pp_pos = self.parking_place.parking_model.inner_body.position

            car_angle = car.car_model.body.angle
            pp_angle = self.parking_place.parking_model.inner_body.angle

            car_speed = car.car_model.body.velocity.get_length_sqrd() ** 0.5

            car.controlling(
                keys,
                [
                    car_pos[0] - pp_pos[0],
                    car_pos[1] - pp_pos[1],
                    car_angle - pp_angle,
                    car_speed,
                ],
            )

        delta_time *= 16

        self.space.step(delta_time)
        self.ticks_elapsed += delta_time
        if self.ticks_elapsed > self.tick_lim:
            self.state = 0

        for i, car in enumerate(self.cars):
            car_pos = car.car_model.body.position
            pp_pos = self.parking_place.parking_model.inner_body.position

            car_angle = car.car_model.body.angle
            pp_angle = self.parking_place.parking_model.inner_body.angle

            dst = (car_pos[0] - pp_pos[0]) * (car_pos[0] - pp_pos[0]) + (
                car_pos[1] - pp_pos[1]
            ) * (car_pos[1] - pp_pos[1])

            car_speed = car.car_model.body.velocity.get_length_sqrd() ** 0.5

            # self.fitnesses[i] +=  -1 + 100 / (dst ** 0.5 + 1) - 10 / (car_speed + 1)
            self.fitnesses[i] += (
                -(dst**0.5)
                - abs(car_angle - pp_angle) * (dst**0.5 / 100)
                + 10000 * int(car.is_car_parked)
            )
            # self.fitnesses[i] +=  1 / (abs(car_angle - pp_angle) + 10) + 100 / (dst ** 0.5 + 1) - 10 / (car_speed + 1)

            car.apply_friction()
            car.sync()

    def draw(self):
        if self.state == 0:
            return

        self.render_group.camera.use()
        self.down_render_group.draw()
        self.render_group.draw()
        self.top_render_group.draw()

        self.screen_group.camera.use()
        self.screen_group.draw()
