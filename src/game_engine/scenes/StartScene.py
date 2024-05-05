import arcade
import arcade.gui
from pyglet.math import Vec2 as Vector2D

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.animator.FloatingAnimator import FloatingAnimator
from src.render.animator.WanderAnimator import WanderAnimator
from src.render.screen_elements.UIAnimatorWidget import UIAnimatableWidget
from src.render.sprites.BasicSprite import BasicSprite


class StartScene:
    def __init__(self, core_instance):
        self.core_instance = core_instance

        #
        # Background
        #

        self.background = BasicSprite("assets/pic/map/Map.jpg", Vector2D(0, 0))
        # self.background = BasicSprite("assets/pic/extra/grass.png", Vector2D(0, 0))
        self.background.update_scale(10)

        self.background_animator = WanderAnimator(
            self.background, limits_x=(-1000, 1000), limits_y=(-1000, 1000), speed=0.05
        )

        #
        # Text
        #

        self.title = arcade.Text(
            "Park me",
            100,
            900,
            arcade.color.BLACK,
            100,
            200,
            "center",
            font_name="Karmatic Arcade",
        )
        self.comment1 = arcade.Text(
            "след от колес машины", 100, 650, arcade.color.BLACK, 20, 200
        )
        self.border_box1 = arcade.SpriteSolidColor(
            500,
            400,
            arcade.color.WHITE,
        )
        self.border_box1.position = (340, 820)
        self.comment2 = arcade.Text(
            "Бэкграунд - парковка, по которой ездит машинка",
            200,
            150,
            arcade.color.BLACK,
            20,
            200,
        )
        self.border_box2 = arcade.SpriteSolidColor(
            630,
            40,
            arcade.color.WHITE,
        )
        self.border_box2.position = (515, 155)

        #
        # Play button
        #

        self.play_button = arcade.gui.UIFlatButton(
            text="Play",
            width=200,
            height=100,
            style={
                "font_name": "Minecraft Ten font cyrillic",
                "font_size": 40,
                "font_color": arcade.color.BLACK,
                "border_color": arcade.color.BLACK,
                "bg_color": arcade.color.WHITE,
            },
        )
        self.play_button.on_click = self.on_click

        self.play_button_animator = UIAnimatableWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.play_button,
            animator_type=FloatingAnimator,
            animator_params={"speed": 1.0},
        )
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager.add(self.play_button_animator)

    def update(self, io_controller, delta_time):
        self.background_animator.update(delta_time)

        self.play_button_animator.update_animation(delta_time)

    def draw(self):
        self.background.draw()

        self.border_box1.draw()
        self.border_box2.draw()

        self.title.draw()

        self.comment1.draw()
        self.comment2.draw()

        self.manager.draw()

    def on_click(self, event):
        self.core_instance.set_scene(GameScene)
