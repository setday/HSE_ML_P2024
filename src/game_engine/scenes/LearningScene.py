import math
import random

import pymunk

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
    def __init__(self, view_mode, spectate_mode):
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

        self.population_size = 100
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

        self.view_mode = view_mode
        self.spectate_mode = spectate_mode

        self.radius = 300
        self.tick_lim = 2 * self.radius / 10

        self.genomes = None
        self.state = -1
        self.ticks_elapsed = 0
        self.gen = 0

        if self.spectate_mode:
            self.selected_id = 0
            self.cars[0].select()
            self.render_group.camera.snap_to_sprite(self.cars[0].car_view)

        self.avg_fit = 0
        self.overall_best = 0

        self.file = open("plot.txt", "w")

        self.iters = 0
        self.prev_pos = []
        self.fitnesses = []

        self.reset()

    def reset(self):
        self.state = 0
        angle = 2 * math.pi * random.random()
        dangle = -math.pi / 2 + math.pi * (
            random.random() / 2 + 0.5
        ) / 4 * random.choice([-1, 1])
        pos = (
            self.radius * math.cos(angle),
            self.radius * math.sin(angle),
        )
        for i in range(self.population_size):
            self.cars[i].car_model.body.position = pos
            self.cars[i].car_model.body.angle = angle + dangle
        self.ticks_elapsed = 0
        self.iters = 0

        self.prev_pos = [self.radius**2 for _ in range(self.population_size)]

        self.fitnesses = [0 for _ in range(self.population_size)]

    def link_models(self, models):
        for i in range(self.population_size):
            self.cars[i].controller.link_model(models[i])

    def link_genomes(self, genomes):
        self.genomes = genomes

    def update_cars_fitness(self):
        self.gen += 1
        self.file.write(
            " ".join(
                [
                    str(self.gen),
                    str(round(max(self.fitnesses), 2)),
                    str(round(sum(self.fitnesses) / self.population_size, 1)),
                ]
            )
            + "\n"
        )
        print(
            " | ".join(
                [
                    f"Gen #{self.gen}",
                    str(self.iters),
                    str(round(max(self.fitnesses), 1)),
                    str(round(sum(self.fitnesses) / self.population_size, 1)),
                    str(round(self.overall_best, 1)),
                    str(round(self.avg_fit / self.gen / self.population_size, 1)),
                ]
            ),
            end="\r",
        )
        self.avg_fit += sum(self.fitnesses)
        self.overall_best = max(self.overall_best, max(self.fitnesses))
        for i, car in enumerate(self.cars):
            car.car_model.body.velocity = (0, 0)
            self.genomes[i][1].fitness = self.fitnesses[i]

    def update(self, io_controller, delta_time):
        if self.state == 0:
            return
        self.iters += 1

        keys = io_controller.keyboard

        for i, car in enumerate(self.cars):
            car_pos = car.car_model.body.position
            pp_pos = self.parking_place.parking_model.inner_body.position

            car_speed = car.car_model.body.velocity.get_length_sqrd() ** 0.5

            car.controlling(
                keys,
                [
                    car_pos[0] - pp_pos[0],
                    car_pos[1] - pp_pos[1],
                    car.car_model.body.angle,
                    self.parking_place.parking_model.inner_body.angle,
                    math.atan2(car_pos[1] - pp_pos[1], car_pos[0] - pp_pos[0]),
                    car_speed,
                ],
            )

        delta_time *= 16

        self.space.step(delta_time)
        self.ticks_elapsed += delta_time
        if self.ticks_elapsed > self.tick_lim:
            self.state = 0

        best = 0
        for i, car in enumerate(self.cars):
            car_pos = car.car_model.body.position
            pp_pos = self.parking_place.parking_model.inner_body.position

            car_angle = car.car_model.body.angle
            pp_angle = self.parking_place.parking_model.inner_body.angle

            dst = (car_pos[0] - pp_pos[0]) * (car_pos[0] - pp_pos[0]) + (
                car_pos[1] - pp_pos[1]
            ) * (car_pos[1] - pp_pos[1])

            def get_ang(car_ang, pp_ang):
                cx, cy = math.cos(car_ang), math.sin(car_ang)
                px, py = math.cos(pp_ang), math.sin(pp_ang)
                ang1 = abs(math.atan2(cy, cx) - math.atan2(py, px))
                ang2 = abs(math.atan2(-cy, -cx) - math.atan2(py, px))
                return min(min(ang1, 2 * math.pi - ang1), min(ang2, 2 * math.pi - ang2))

            self.fitnesses[i] += (
                0.1 * (self.prev_pos[i] - dst) / self.radius
                + self.radius / (dst + 5)
                + 10000 * car.is_car_parked
                + get_ang(car_angle, pp_angle) / (math.pi / 2)
            )
            self.prev_pos[i] = dst

            if self.view_mode and self.fitnesses[i] > self.fitnesses[best]:
                best = i

            car.apply_friction()
            car.sync()

        if self.spectate_mode:
            self.cars[self.selected_id].deselect()
            self.selected_id = best
            self.cars[self.selected_id].select()
            self.render_group.camera.snap_to_sprite(
                self.cars[self.selected_id].car_view
            )

    def draw(self):
        if self.state == 0:
            return

        if self.view_mode:
            self.render_group.camera.use()
            self.down_render_group.draw()
            self.render_group.draw()
            self.top_render_group.draw()

            self.screen_group.camera.use()
            self.screen_group.draw()
