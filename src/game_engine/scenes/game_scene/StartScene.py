import arcade
from src.render.sprites.BasicRect import BasicRect
from src.render.sprites.BasicSprite import BasicSprite
import arcade.gui
from pyglet.math import Vec2 as Vector2D


class StartScene:
    def __init__(self):
        self.background = BasicSprite("assets/pic/Map.jpg", Vector2D(0, 0))
        self.background.update_scale(10)
        self.title = arcade.Text(
            "Park me",
            100,
            900,
            arcade.color.BROWN,
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
            300,
            40,
            arcade.color.WHITE,
        )
        self.border_box1.position = (245, 655)
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
                "font_color": arcade.color.RED,
                "border_color": arcade.color.WHITE,
                "bg_color": arcade.color.BLUE
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
        self.game_started = False

    def draw(self):
        self.background.draw()
        self.title.draw()
        self.border_box1.draw()
        self.comment1.draw()
        self.border_box2.draw()
        self.comment2.draw()
        self.manager.draw()

    def on_click(self, event):
        self.game_started = True
