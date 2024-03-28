import arcade
import arcade.gui
from pyglet.math import Vec2 as Vector2D

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.sprites.BasicSprite import BasicSprite


class StartScene:
    def __init__(self, core_instance):
        self.core_instance = core_instance

        self.background = BasicSprite("assets/pic/map/Map.jpg", Vector2D(0, 0))
        self.background.update_scale(10)
        self.title = arcade.Text(
            "Park me",
            100,
            900,
            arcade.color.BLACK,
            100,
            200,
            'center',
            font_name="Karmatic Arcade"
        )
        self.comment1 = arcade.Text(
            "след от колес машины",
            100,
            650,
            arcade.color.BLACK,
            20,
            200
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
            200
        )
        self.border_box2 = arcade.SpriteSolidColor(
            630,
            40,
            arcade.color.WHITE,
        )
        self.border_box2.position = (515, 155)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.play_button = arcade.gui.UIFlatButton(
            text="Play",
            width=200,
            height=100,
            style={
                "font_name": 'Minecraft Ten font cyrillic',
                "font_size": 40,
                "font_color": arcade.color.BLACK,
                "border_color": arcade.color.BLACK,
                "bg_color": arcade.color.WHITE,
            }
        )
        self.play_button.on_click = self.on_click
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.play_button
            )
        )

    def update(self, io_controller, delta_time):
        pass

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
