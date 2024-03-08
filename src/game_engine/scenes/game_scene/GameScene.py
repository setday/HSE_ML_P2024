import random
import time

import arcade
import pymunk

from pyglet.math import Vec2 as Vector2D

from src.game_engine.entities.Car import Car
from src.game_engine.entities.Indicator import Indicator
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite


class GameScene:
    def __init__(self):
        self.render_group = RenderGroup()
        self.space = pymunk.Space()
        self.emitter = []
        self.score = 10000

        def collision_car_with_car(arbiter, space, data):
            car1: Car = arbiter.shapes[0].super
            car2: Car = arbiter.shapes[1].super
            delta_score = 10 #(car1.car_model.body.velocity - car2.car_model.body.velocity).get_length_sqrd() / 30
            self.score -= delta_score

            if car1.car_model.body.velocity.get_length_sqrd() > 10:
                self.create_debris_effect(random.choice(arbiter.contact_point_set.points).point_a)

            health_decreation = delta_score
            car1.health -= health_decreation
            car2.health -= health_decreation
            return True

        def collision_car_with_O(arbiter, space, data):
            car = arbiter.shapes[0].super
            cone = arbiter.shapes[1].super
            if isinstance(cone, Car):
                car, cone = cone, car
            if isinstance(cone, StaticObstacle):
                delta_score = health_decreation = 10  # car.car_model.body.velocity.get_length_sqrd() / 50
                self.score -= delta_score
                self.create_debris_effect(arbiter.contact_point_set.points[0].point_a)
                car.health -= health_decreation
                return True
            delta_score = health_decreation = 5
            self.score -= delta_score
            cone.health -= health_decreation
            if cone.health <= 0:
                self.create_debris_effect(arbiter.contact_point_set.points[0].point_a)
                cone.remove()
            return True

        h = self.space.add_collision_handler(10, 10)
        h.begin = collision_car_with_car
        h = self.space.add_collision_handler(10, 20)
        h.begin = collision_car_with_O
        h = self.space.add_collision_handler(10, 30)
        h.begin = collision_car_with_O

        self.background = BasicSprite("assets/Map.jpg", (0, 0))
        self.background.update_scale(10)

        self.render_group.add(self.background)

        self.car_m = Car(self.render_group, self.space, (0, -100), 0)
        self.indicator = Indicator(self.car_m)
        self.render_group.add(self.indicator.sprite_list)
        self.cars = [self.car_m]
        for i in range(-5, 5):
            if i == 0:
                continue
            self.cars.append(Car(self.render_group, self.space, (70 * i, -100), 1))

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
            StaticObstacle(self.render_group, self.space, (70 * i, -10))

        self.render_group.camera.snap_to_sprite(self.car_m.car_view)

    def update(self, keys, delta_time):
        if keys.get(arcade.key.LEFT, False) or keys.get(arcade.key.A, False):
            self.car_m.turn_left(keys.get(arcade.key.SPACE, False))
        if keys.get(arcade.key.RIGHT, False) or keys.get(arcade.key.D, False):
            self.car_m.turn_right(keys.get(arcade.key.SPACE, False))
        if keys.get(arcade.key.UP, False) or keys.get(arcade.key.W, False):
            self.car_m.accelerate()
        if keys.get(arcade.key.DOWN, False) or keys.get(arcade.key.S, False):
            self.car_m.brake()
        if keys.get(arcade.key.R, False):
            self.car_m.car_model.body.velocity = (0, 0)

        if keys.get(arcade.key.SPACE, False):
            self.car_m.hand_brake()

        for car in self.cars:
            if car == self.car_m:
                continue
            car.hand_brake()

        delta_time *= 16

        self.space.step(delta_time)

        for car in self.cars:
            car.apply_friction()
            car.sync()

        for cone in self.traffic_cones:
            cone.apply_friction()
            cone.sync()
        self.indicator.set_position(
            self.render_group.camera.get_position(1, 1) - Vector2D(200, 100)
        )
        self.render_group.camera.set_zoom(1 + self.car_m.car_model.body.velocity.get_length_sqrd() / 10000)
        for emitter in self.emitter:
            emitter.update()
        while len(self.emitter) > 0 and self.emitter[0].get_count() == 0:
            self.emitter.pop(0)
        self.indicator.update_bar()

    def draw(self):
        self.render_group.draw()
        for emitter in self.emitter:
            emitter.draw()
        self.render_group.camera.use()

    def create_debris_effect(self, center):
        x, y = center

        self.emitter.append(arcade.make_burst_emitter(
            center_xy=(x, -y),
            filenames_and_textures=(":resources:images/pinball/pool_cue_ball.png",
                                    ":resources:images/space_shooter/meteorGrey_big2.png"),
            particle_count=5,
            particle_speed=0.3,
            particle_lifetime_min=0.75,
            particle_lifetime_max=1.25,
            particle_scale=0.13,
            fade_particles=True
        ))
