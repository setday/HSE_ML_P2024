import time

import arcade.key
from arcade.experimental import Shadertoy
import pymunk
from pyglet.math import Vec2 as Vector2D

from src.game_engine.controllers.Controller import *
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.scenes.game_scene.CollisionHandlers import collision_car_with_car, collision_car_with_obstacle
from src.render.RenderGroup import RenderGroup
from src.render.particle.ParticleShow import ParticleShow
from src.render.screen_elements.Indicator import Indicator
from src.render.screen_elements.ScoreDisplay import ScoreDisplay
from src.render.sprites.BasicSprite import BasicSprite


class GameScene:
    def __init__(self, core_instance):
        self.core_instance = core_instance

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

        self.background = BasicSprite("assets/pic/map/Map.jpg", Vector2D(0, 0))
        self.background.update_scale(10)

        self.down_render_group.add(self.background)

        self.car_m = ObjectFactory.create_object(render_group=self.render_group,
                                                 space=self.space,
                                                 object_type='car',
                                                 position=Vector2D(0, -100),
                                                 car_model='blue_car')

        self.car_m.switch_controller(KeyboardController())

        self.render_group.camera.snap_to_sprite(self.car_m.car_view)

        self.cars = [self.car_m]
        for i in range(-5, 5):
            if i == 0:
                continue
            car = ObjectFactory.create_object(render_group=self.render_group,
                                              space=self.space,
                                              object_type='car',
                                              position=Vector2D(70 * i, -100),
                                              car_model='red_car')
            car.switch_controller(random.choice([RandomController(), AIController(), BrakeController()]))
            self.cars.append(car)

        self.traffic_cones = []
        for i in range(-5, 5):
            self.traffic_cones.append(
                ObjectFactory.create_object(
                    render_group=self.render_group,
                    space=self.space,
                    object_type='movable_obstacle',
                    position=Vector2D(70 * i, -170),
                    movable_obstacle_model='cone'
                )
            )

        self.traffic_cones.append(ObjectFactory.create_object(
            self.render_group, self.space, 'movable_obstacle', Vector2D(70 * -5 - 35, -70),
            movable_obstacle_model='cone'
        ))
        self.traffic_cones.append(ObjectFactory.create_object(
            self.render_group, self.space, 'movable_obstacle', Vector2D(70 * -5 - 40, -100),
            movable_obstacle_model='cone'
        ))
        self.traffic_cones.append(ObjectFactory.create_object(
            self.render_group, self.space, 'movable_obstacle', Vector2D(70 * -5 - 35, -130),
            movable_obstacle_model='cone'
        ))

        self.traffic_cones.append(ObjectFactory.create_object(
            self.render_group, self.space, 'movable_obstacle', Vector2D(70 * 4 + 35, -70),
            movable_obstacle_model='cone'
        ))
        self.traffic_cones.append(ObjectFactory.create_object(
            self.render_group, self.space, 'movable_obstacle', Vector2D(70 * 4 + 40, -100),
            movable_obstacle_model='cone'
        ))
        self.traffic_cones.append(ObjectFactory.create_object(
            self.render_group, self.space, 'movable_obstacle', Vector2D(70 * 4 + 35, -130),
            movable_obstacle_model='cone'
        ))

        for i in range(-5, 5):
            ObjectFactory.create_object(
                self.top_render_group, self.space, 'static_obstacle', Vector2D(70 * i, -10),
                static_obstacle_model='tree'
            )

        for i in range(-5, 4):
            ObjectFactory.create_object(
                self.render_group, self.space, 'static_obstacle', Vector2D(70 * i + 35, -100), 90,
                static_obstacle_model='metal_pipe'
            )
        for i in range(-5, 5):
            ObjectFactory.create_object(
                self.render_group, self.space, 'static_obstacle', Vector2D(70 * i, -50),
                static_obstacle_model='rubbish_line'
            )

        ObjectFactory.create_object(
            self.render_group, self.space, 'static_obstacle', Vector2D(0, 1000),
            static_obstacle_model='x_barrier'
        )
        ObjectFactory.create_object(
            self.render_group, self.space, 'static_obstacle', Vector2D(0, -2000),
            static_obstacle_model='x_barrier'
        )
        ObjectFactory.create_object(
            self.render_group, self.space, 'static_obstacle', Vector2D(3500, 0),
            static_obstacle_model='y_barrier'
        )
        ObjectFactory.create_object(
            self.render_group, self.space, 'static_obstacle', Vector2D(-3500, 0),
            static_obstacle_model='y_barrier'
        )

        ######################
        # Screen Elements
        ######################

        self.screen_group = RenderGroup()
        camera_offset = self.screen_group.camera.get_position(1, 1)

        self.indicator = Indicator(owner=self.car_m, position=camera_offset - Vector2D(200, 100))
        self.screen_group.add(self.indicator.sprite_list)

        self.score_board = ScoreDisplay(score=self.score[0], position=camera_offset - Vector2D(200, 170),
                                        color=(255, 220, 40),
                                        font_path='assets/fnt/ka1.ttf', font_name='Karmatic Arcade')
        self.screen_group.add(self.score_board.sprite_list)

        camera_offset = self.screen_group.camera.get_position(0, 0)
        self.end_text = arcade.Text(
            "ENDDDDDDD",
            camera_offset.x,
            camera_offset.y,
            arcade.color.WHITE,
            100,
            anchor_x="center",
            anchor_y="center",
            font_name="Karmatic Arcade"
        )

        ######################
        # Shaders Setup
        ######################
        # file = open("src/shaders/toy/fractal_pyramid.glsl")
        file = open("src/shaders/vignette/vignette.glsl")
        shader_sourcecode = file.read()
        self.shader_vin = Shadertoy((1920, 1080), shader_sourcecode)

        file = open("src/shaders/color_filters/grayscale.glsl")
        shader_sourcecode = file.read()
        self.shader_gray = Shadertoy((1920, 1080), shader_sourcecode)

        self.tick = 0
        self.reset_timer = 7

    def update(self, io_controller, delta_time):
        keys = io_controller.keyboard

        if keys.get(arcade.key.F6, False):
            image = arcade.get_image()
            image.save(f"data/screenshots/{time.time()}.png")

        if keys.get(arcade.key.F7, False):
            self.car_m.health = 100

        if keys.get(arcade.key.F8, False):
            self.car_m.health = 10

        self.car_m.controlling(keys)

        for car in self.cars:
            if car == self.car_m:
                continue
            car.controlling(keys)

        self.space.step(delta_time * 16)

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

        if self.car_m.health <= 0:
            self.reset_timer -= delta_time

            if self.reset_timer <= 0:
                self.core_instance.set_scene(None)

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

        ######################
        # Shaders Draw
        ######################

        self.tick += 1

        self.shader_vin.render(time=self.tick / 125, time_delta=self.car_m.health, mouse_position=(0, 0))

        if self.car_m.health <= 0:
            first_black_screen_trans = min((7.0 - self.reset_timer) * 0.6, 0.8)
            self.shader_gray.render(time=first_black_screen_trans, mouse_position=(0, 0))

            text_len = int(max((6.0 - self.reset_timer) * 7, 0.0))
            self.end_text.text = "You   LOSE"[:text_len]
            self.end_text.draw()

            last_black_screen_trans = (3.0 - self.reset_timer) * 0.6
            self.shader_gray.render(time=last_black_screen_trans, mouse_position=(0, 0))
