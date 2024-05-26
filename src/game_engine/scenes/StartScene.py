import arcade
import arcade.gui
from pyglet.math import Vec2 as Vector2D
from pyglet import gl

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.animator.FloatingAnimator import FloatingAnimator
from src.render.animator.WanderAnimator import WanderAnimator
from src.render.screen_elements.UIAnimatorWidget import UIAnimatableWidget
from src.render.sprites.BasicSprite import BasicSprite
from src.utils.Loaders import load_texture


class StartScene:
    def __init__(self, core_instance):
        self.core_instance = core_instance

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        #
        # Background
        #

        self.background = BasicSprite("assets/pic/map/Map.jpg", Vector2D(0, 0))
        # self.background = BasicSprite("assets/pic/extra/grass.png", Vector2D(0, 0))
        self.background.update_scale(10)

        self.background_animator = WanderAnimator(
            self.background, limits_x=(-1000, 1000), limits_y=(-1000, 1000), speed=0.05
        )

        ###
        # Main Menu
        ###

        #
        # Text
        #

        self.title = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/Logo.png"),
            width=98 * 7,
            height=64 * 7,
        )
        self.title_animator = UIAnimatableWidget(
            anchor_x="center",
            anchor_y="top",
            align_y=-50,
            child=self.title,
            animator_type=FloatingAnimator,
            animator_params={"speed": 1.0},
        )
        self.manager.add(self.title_animator)

        #
        # Play button
        #

        self.play_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/PLAY.png"),
            texture_hovered=load_texture("assets/pic/buttons/PLAY_hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/PLAY_pressed.png"),
            width=74,
            height=18,
            scale=9,
            style={
                "border_color": arcade.color.BLACK,
                "bg_color": arcade.color.WHITE,
            },
        )
        self.play_button.on_click = self.start_game

        self.credits_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/CREDITS.png"),
            texture_hovered=load_texture("assets/pic/buttons/CREDITS_hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/CREDITS_pressed.png"),
            width=74,
            height=18,
            scale=9,
            style={
                "border_color": arcade.color.BLACK,
                "bg_color": arcade.color.WHITE,
            },
        )
        self.credits_button.on_click = self.open_credits

        self.button_group = arcade.gui.UIBoxLayout(
            children=[self.play_button, self.credits_button],
            space_between=20,
        )

        self.button_animator = UIAnimatableWidget(
            anchor_x="center",
            anchor_y="bottom",
            align_y=150,
            child=self.button_group,
            animator_type=FloatingAnimator,
            animator_params={"speed": 1.0},
        )
        self.manager.add(self.button_animator)

        ###
        # Credits
        ###

        self.credits = arcade.gui.UITextArea(
            text="Made with love by:\n"
            "  - Matheus de Andrade\n"
            "  - Gabriel de Andrade:"
            "  - Gabriel de Andrade\n",
            width=2000,
            height=2000,
            text_color=arcade.color.WHITE,
            font_size=100,
            # 200,
            # "center",
            # font_name="Karmatic Arcade",
        )
        self.credits_wrapper = arcade.gui.UIAnchorWidget(
            anchor_x="center",
            anchor_y="center",
            child=self.credits,
        )

        self.manager.add(self.credits_wrapper)

    def update(self, io_controller, delta_time):
        self.background_animator.update(delta_time)

        self.button_animator.update_animation(delta_time)
        self.title_animator.update_animation(delta_time)

    def draw(self):
        self.background.draw()

        self.manager.draw()

    def start_game(self, event):
        self.core_instance.set_scene(GameScene)

    def open_credits(self, event):
        #move screen left
        pass
