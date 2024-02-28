import time

import arcade
import pymunk

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
        self.emitter = None
        self.score = 10000

        def collision_car_with_car(arbiter, space, data):
            car1: Car = arbiter.shapes[0].super
            car2: Car = arbiter.shapes[1].super

            delta_score = (car1.car_model.body.velocity - car2.car_model.body.velocity).get_length_sqrd() / 30
            self.score -= delta_score

            health_decreation = max(0, delta_score - 1)
            car1.health -= health_decreation
            car2.health -= health_decreation
            return True

        def collision_car_with_O(arbiter, space, data):
            car = arbiter.shapes[0].super
            cone = arbiter.shapes[1].super
            if isinstance(cone, Car):
                car, cone = cone, car
            delta_score = car.car_model.body.velocity.get_length_sqrd() / 50
            self.score -= delta_score
            health_decreation = max(0, delta_score - 1)
            car.health -= health_decreation
            if isinstance(cone, StaticObstacle):
                self.make_emitter(cone.obstacle_view.center_x, cone.obstacle_view.center_y)
                return True
            cone.health -= health_decreation
            if cone.health <= 0:
                self.make_emitter(cone.obstacle_view.center_x, cone.obstacle_view.center_y)
                cone.obstacle_view.remove_from_sprite_lists()
                cone.obstacle_boundary.remove_from_sprite_lists()
                self.space.remove(cone.obstacle_model.body, cone.obstacle_model.shape)
            return True

        h = self.space.add_collision_handler(10, 10)
        h.begin = collision_car_with_car
        h = self.space.add_collision_handler(10, 20)
        h.begin = collision_car_with_O
        h = self.space.add_collision_handler(10, 30)
        h.begin = collision_car_with_O

        self.background = BasicSprite("../assets/Map.jpg", (0, 0))
        self.background.update_scale(10)

        self.render_group.add(self.background)

        self.car_m = Car(self.render_group, self.space, (0, -100), 0)
        self.car_m.set_indicator(Indicator(self.car_m, self.render_group))
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
        self.car_m.indicator.set_position(
            (self.render_group.camera.position[0] + 700 * self.render_group.camera.scale,
             self.render_group.camera.position[1] + 700 * self.render_group.camera.scale)
        )
        self.car_m.indicator.set_fullness(self.car_m.health / 100)
        self.render_group.camera.set_zoom(1 + self.car_m.car_model.body.velocity.get_length_sqrd() / 10000)
        if self.emitter:
            self.emitter.update()

    def draw(self):
        self.render_group.draw()
        if self.emitter:
            self.emitter.draw()
        self.render_group.camera.use()

    def make_emitter(self, center_x, center_y):
        self.emitter = arcade.make_interval_emitter(
            center_xy=(center_x, center_y),
            filenames_and_textures=(":resources:images/pinball/pool_cue_ball.png",
                                    ":resources:images/space_shooter/meteorGrey_big2.png"),
            emit_interval=0.001,
            emit_duration=0.1,
            particle_speed=4,
            particle_lifetime_min=0.1,
            particle_lifetime_max=0.3,
            particle_scale=0.2,
            fade_particles=True
        )
