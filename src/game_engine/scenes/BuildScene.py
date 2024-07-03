import json
import math
import random

import arcade
import arcade.gui
import pymunk
from arcade.gui import UILayout
from pymunk import CollisionHandler, Vec2d
from pyglet.math import Vec2 as Vector2D, Vec2  # type: ignore[import-untyped]

import src.game_engine.scenes.game_scene.CollisionHandlers as CollisionHandlers
from src.game_engine.controllers import KeyboardController
from src.game_engine.entities.Car import Car
from src.game_engine.entities.ObjectFactory import ObjectFactory
from src.game_engine.entities.ParkingPlace import ParkingPlace
from src.game_engine.entities.obstacles.MovableObstacle import MovableObstacle
from src.game_engine.entities.obstacles.StaticObstacle import StaticObstacle
from src.render.Window import IOController
from src.render.particle import ParticleShow
from src.render.scene_elements import RenderGroup
from src.render.screen_elements.effect_animator import (
    EffectAnimator,
)

from src.game_engine.entities.MusicPlayer import stop_all_players
from src.render.screen_elements.ui_components.ui_sprites.NavCircle import NavCircle
from src.render.screen_elements.ui_components.ui_widgets.UICheckButton import (
    UICheckButton,
    make_radio_from_check_buttons,
)
from src.render.screen_elements.ui_components.ui_widgets.UIFullScreenLayout import (
    UIFullScreenLayout,
)
from src.render.screen_elements.ui_components.ui_widgets.UISuperAnchorWidget import (
    UISuperAnchorWidget,
)
from src.render.screen_elements.ui_components.ui_widgets.UITexture import UITexture
from src.render.sprites import BasicSprite
from src.utils import load_texture


class BuildScene:
    def __init__(self, core_instance) -> None:
        self.core_instance = core_instance

        self.space = pymunk.Space()

        ######################
        # Setup scene if needed
        ######################

        self.down_render_group: RenderGroup = RenderGroup()
        self.render_group: RenderGroup = RenderGroup()
        self.top_render_group: RenderGroup = RenderGroup()

        self.car_m = None
        self.cars = []
        self.traffic_cones = []
        self.parking_place = None

        self.objects = []

        ######################
        # Screen Elements
        ######################

        self.screen_group: RenderGroup = RenderGroup()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.button_objects: list[tuple[str, str]] = [
            ("assets/pic/cars/car_2.png", "car_m"),
            ("assets/pic/cars/car_3.png", "car_e"),
            ("assets/pic/marking/parking_place_face.png", "parking"),
            ("assets/pic/obstacles/Traffic_Cone.png", "cone"),
            ("assets/pic/obstacles/Tree_1.png", "tree"),
            ("assets/pic/obstacles/parking_barrier_1.png", "barrier_1"),
            ("assets/pic/obstacles/parking_barrier_2.png", "barrier_2"),
            ("assets/pic/obstacles/parking_barrier_3.png", "barrier_3"),
            ("assets/pic/icon/coin.png", "coin"),
        ]
        self.objects_extra: list[tuple[RenderGroup, str, str]] = [
            (self.render_group, "car", "blue_car"),
            (self.render_group, "car", "red_car"),
            (self.render_group, "parking_place", None),
            (self.render_group, "movable_obstacle", "cone"),
            (self.top_render_group, "static_obstacle", "tree"),
            (self.render_group, "static_obstacle", "metal_pipe"),
            (self.render_group, "static_obstacle", "rubbish_line"),
            (self.render_group, "static_obstacle", "really_long_pipe"),
            (self.render_group, "movable_obstacle", "coin"),
        ]

        selector_buttons = []
        radio_buttons = []
        for texture, name in self.button_objects:
            sb, rb = self.load_object_button(texture, name)
            selector_buttons.append(sb)
            radio_buttons.append(rb)
        make_radio_from_check_buttons(radio_buttons, lambda x: self.switch_object(x))

        game_selector_layout = UIFullScreenLayout(
            children=[
                arcade.gui.UIAnchorWidget(
                    child=arcade.gui.UIBoxLayout(
                        children=selector_buttons,
                        space_between=80,
                        vertical=False,
                    ),
                    anchor_x="left",
                    anchor_y="bottom",
                    align_y=75,
                    align_x=75,
                )
            ]
        )

        self.manager.add(game_selector_layout)

        ######################
        # Effects
        ######################

        self.is_destroyed = False

        self.background = BasicSprite("assets/pic/map/Map.jpg")
        self.down_render_group.add(self.background)

        self.type_id = 0
        self.current_object = BasicSprite("assets/pic/cars/car_2.png", (0, 0))
        self.top_render_group.add(self.current_object)

        self.time = 0

    def load_object_button(self, texture: str, name: str) -> (UILayout, UICheckButton):
        chk_bt = UICheckButton(
            textures_checked=(
                load_texture("assets/pic/buttons/presets/Button_narrow_pressed.png"),
                load_texture("assets/pic/buttons/presets/Button_narrow_pressed.png"),
                load_texture("assets/pic/buttons/presets/Button_narrow.png"),
            ),
            textures_unchecked=(
                load_texture("assets/pic/buttons/presets/Button_narrow.png"),
                load_texture("assets/pic/buttons/presets/Button_narrow_hovered.png"),
                load_texture("assets/pic/buttons/presets/Button_narrow_pressed.png"),
            ),
            scale=7,
        )
        spr_texture = UITexture(
            texture=load_texture(texture),
            max_height=int(chk_bt.height * 0.55),
            max_width=int(chk_bt.width * 0.65),
        )
        txt_name = arcade.gui.UILabel(
            text=name,
            color=arcade.color.WHITE,
            font_size=20,
            align="center",
            height=int(chk_bt.height * 0.3),
        )
        return (
            UILayout(
                children=[
                    arcade.gui.UIAnchorWidget(
                        child=chk_bt,
                        anchor_x="center",
                        anchor_y="center",
                    ),
                    arcade.gui.UIAnchorWidget(
                        child=spr_texture,
                        anchor_x="center",
                        anchor_y="center",
                    ),
                    arcade.gui.UIAnchorWidget(
                        child=txt_name,
                        anchor_x="center",
                        anchor_y="bottom",
                        align_y=-25,
                    ),
                ]
            ),
            chk_bt,
        )

    def do_destroy(self):
        self.core_instance = None

        self.manager.disable()
        self.manager = None

        self.down_render_group = None
        self.render_group = None
        self.top_render_group = None
        self.screen_group = None

        self.car_m = None
        self.cars = None
        self.traffic_cones = None
        self.parking_place = None

        self.background = None

        self.is_destroyed = True

        stop_all_players()

    def update(self, io_controller: IOController, delta_time: float) -> None:
        if self.is_destroyed:
            raise Exception("Scene is destroyed")

        delta_time = min(delta_time, 0.1)
        self.time += delta_time

        if self.is_destroyed:
            return

        m_x, m_y = io_controller.mouse_position
        m_x *= self.render_group.camera.scale
        m_y *= self.render_group.camera.scale

        c_x, c_y = self.render_group.camera.get_position(-1, -1, True)
        s_x, s_y = io_controller.mouse_scroll_delta

        self.current_object.position = (m_x + c_x, m_y + c_y)
        if io_controller.is_key_pressed(arcade.key.LALT):
            self.current_object.angle += s_y * 2.0
        elif io_controller.is_key_pressed(arcade.key.LCTRL):
            self.render_group.camera.zoom_times(1 + s_y * 0.1)
        else:
            if io_controller.is_key_pressed(arcade.key.LSHIFT):
                s_x, s_y = s_y, s_x
            self.render_group.camera.slide(Vec2(s_x * 30, s_y * 30))

        if io_controller.is_key_pressed(arcade.key.W):
            self.render_group.camera.slide(Vec2(0, 30))
        if io_controller.is_key_pressed(arcade.key.S):
            self.render_group.camera.slide(Vec2(0, -30))
        if io_controller.is_key_pressed(arcade.key.A):
            self.render_group.camera.slide(Vec2(-30, 0))
        if io_controller.is_key_pressed(arcade.key.D):
            self.render_group.camera.slide(Vec2(30, 0))

        if io_controller.is_mouse_clicked(arcade.MOUSE_BUTTON_LEFT):
            p_x, p_y = self.current_object.position

            obj = ObjectFactory.create_object(
                render_group=self.objects_extra[self.type_id][0],
                space=self.space,
                position=(p_x, -p_y),
                angle=-self.current_object.angle,
                is_main_car=self.type_id == 0,
                object_type=self.objects_extra[self.type_id][1],
                car_model=self.objects_extra[self.type_id][2],
                static_obstacle_model=self.objects_extra[self.type_id][2],
                movable_obstacle_model=self.objects_extra[self.type_id][2],
            )
            obj.model_type = self.objects_extra[self.type_id][1]
            obj.model_data = self.objects_extra[self.type_id][2]
            obj.model_angle = -self.current_object.angle
            obj.model_position = (p_x, -p_y)
            self.objects.append(obj)

        if io_controller.is_key_clicked(arcade.key.U):
            self.dump_scene(f"assets/maps/scene_{int(self.time * 1000)}.json")

        self.current_object.alpha = int(170 + 64 * math.sin(self.time * 4))

        self.update_env(io_controller, delta_time)
        self.update_screen()

    def switch_object(self, obj_id: int):
        self.type_id = obj_id
        self.current_object.texture = load_texture(self.button_objects[obj_id][0])

    def dump_scene(self, path: str):
        data = {
            "version": "2.0",
            "background": {
                "path": "!!! Unknown !!!",
                "pos": (0, 0),
                "scl": 0.0,
            },
            "cars": [],
            "parking_places": [],
            "static_obstacles": [],
            "movable_obstacles": [],
        }

        for obj in self.objects:
            data_record = {
                "pos": obj.model_position,
                "ang": obj.model_angle,
            }
            if obj.model_data and obj.model_data != "blue_car":
                data_record["mdl"] = obj.model_data
            if obj.model_type == "car" and obj.is_main_car:
                data_record["is_main_car"] = obj.is_main_car
            data[obj.model_type + "s"].append(data_record)

        with open(path, "w") as file:
            file.write(json.dumps(data, indent=2))

    def update_env(self, io_controller: IOController, delta_time: float) -> None:
        pass

    def update_screen(self):
        ######################
        # Screen Elements Update
        ######################

        pass

    def draw(self) -> None:
        self.draw_env()
        self.draw_screen_elements()

    def draw_env(self):
        ######################
        # Environment Draw
        ######################

        self.render_group.camera.use()
        self.down_render_group.draw()
        for car in self.cars:
            for emitter in car.tyre_emitters:
                emitter.draw()
        self.render_group.draw()
        self.top_render_group.draw()

    def draw_screen_elements(self):
        ######################
        # Screen Elements Draw
        ######################

        self.screen_group.camera.use()

        self.manager.draw()
        self.screen_group.draw()
