import arcade
import arcade.gui
from pyglet.math import Vec2 as Vector2D
from pyglet import gl

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.animator.FloatingAnimator import FloatingAnimator
from src.render.animator.WanderAnimator import WanderAnimator
from src.render.screen_elements.UIAnimatorWidget import UIAnimatableWidget, UIFullScreenLayout, UISuperAnchorWidget
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

        self.title_animator = UIAnimatableWidget(
            anchor_x="center",
            anchor_y="top",
            align_y=-50,
            child=arcade.gui.UITextureButton(
                texture=load_texture("assets/pic/Logo.png"),
                width=98 * 7,
                height=64 * 7,
            ),
            animator_type=FloatingAnimator,
            animator_params={"speed": 1.0},
        )

        #
        # Play button
        #

        self.play_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/PLAY.png"),
            texture_hovered=load_texture("assets/pic/buttons/PLAY_hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/PLAY_pressed.png"),
            width=74,
            height=18,
            scale=9
        )
        self.play_button.on_click = self.go_game_selector

        self.credits_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/CREDITS.png"),
            texture_hovered=load_texture("assets/pic/buttons/CREDITS_hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/CREDITS_pressed.png"),
            width=74,
            height=18,
            scale=9
        )
        self.credits_button.on_click = self.go_credits

        self.button_animator = UIAnimatableWidget(
            anchor_x="center",
            anchor_y="bottom",
            align_y=150,
            relative_x=True,
            child=arcade.gui.UIBoxLayout(
                children=[self.play_button, self.credits_button],
                space_between=20,
            ),
            animator_type=FloatingAnimator,
            animator_params={"speed": 1.0},
        )

        self.main_screen_layout = UIFullScreenLayout(
            children=[self.title_animator, self.button_animator]
        )

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

        self.credits_back_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/BACK.png"),
            texture_hovered=load_texture("assets/pic/buttons/BACK_hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/BACK_pressed.png"),
            width=74,
            height=18,
            scale=9
        )
        self.credits_back_button.on_click = self.go_main

        self.credits_layout = UIFullScreenLayout(
            children=[
                arcade.gui.UIAnchorWidget(child=self.credits_back_button)
            ]
        )

        ###
        # Game Selector
        ###

        self.credits_back_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/BACK.png", flipped_horizontally=True),
            texture_hovered=load_texture("assets/pic/buttons/BACK_hovered.png", flipped_horizontally=True),
            texture_pressed=load_texture("assets/pic/buttons/BACK_pressed.png", flipped_horizontally=True),
            width=74,
            height=18,
            scale=9
        )
        self.credits_back_button.on_click = self.go_main

        self.game_one_button = arcade.gui.UIFlatButton(
            text="Game 1",
            width=300,
            height=100,
            font_size=30,
            # font_name="Karmatic Arcade",
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.BLUE,
                "hover_font_color": arcade.color.WHITE,
                "hover_bg_color": arcade.color.BLUE,
                "clicked_font_color": arcade.color.WHITE,
                "clicked_bg_color": arcade.color.BLUE,
            }
        )
        self.game_one_button.on_click = self.start_game

        self.game_two_button = arcade.gui.UIFlatButton(
            text="Game 2",
            width=300,
            height=100,
            font_size=30,
            # font_name="Karmatic Arcade",
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.BLUE,
                "hover_font_color": arcade.color.WHITE,
                "hover_bg_color": arcade.color.BLUE,
                "clicked_font_color": arcade.color.WHITE,
                "clicked_bg_color": arcade.color.BLUE,
            }
        )
        self.game_two_button.on_click = self.no_game

        self.game_three_button = arcade.gui.UIFlatButton(
            text="Game 3",
            width=300,
            height=100,
            font_size=30,
            # font_name="Karmatic Arcade",
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.BLUE,
                "hover_font_color": arcade.color.WHITE,
                "hover_bg_color": arcade.color.BLUE,
                "clicked_font_color": arcade.color.WHITE,
                "clicked_bg_color": arcade.color.BLUE,
            }
        )
        self.game_three_button.on_click = self.no_game

        self.game_selector_layout = UIFullScreenLayout(
            children=[arcade.gui.UIAnchorWidget(
                child=arcade.gui.UIBoxLayout(
                    children=[self.game_one_button, self.game_two_button, self.game_three_button, self.credits_back_button],
                    space_between=20,
                )
            )]
        )

        ###
        # Screen Layout
        ###

        self.screen_layout = UISuperAnchorWidget(
            anchor_x="center",
            anchor_y="center",
            relative_x=True,
            relative_y=True,
            child=arcade.gui.UIBoxLayout(
                children=[self.credits_layout, self.main_screen_layout, self.game_selector_layout],
                vertical=False
            ),
        )
        self.manager.add(self.screen_layout)

        self._target_offset = 0

    def update(self, io_controller, delta_time):
        self.background_animator.update(delta_time)

        self.button_animator.update_animation(delta_time)
        self.title_animator.update_animation(delta_time)

        self.screen_layout.align_x += (self._target_offset - self.screen_layout.align_x) * 0.1

    def draw(self):
        self.background.draw()

        self.manager.draw()

    def start_game(self, event):
        self.core_instance.set_scene(GameScene)

    def no_game(self, event):
        print("No game found.")

    def go_credits(self, event):
        self._target_offset = 1

    def go_main(self, event):
        self._target_offset = 0

    def go_game_selector(self, event):
        self._target_offset = -1
