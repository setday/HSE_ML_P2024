import arcade
import arcade.gui
from pyglet.math import Vec2 as Vector2D

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.animator.FloatingAnimator import FloatingAnimator
from src.render.animator.WanderAnimator import WanderAnimator
from src.render.screen_elements.UIAnimatorWidget import UIAnimatableWidget
from src.render.screen_elements.UIFullScreenLayout import UIFullScreenLayout
from src.render.screen_elements.UISuperAnchorWidget import UISuperAnchorWidget
from src.render.screen_elements.UISuperText import UISuperText
from src.render.screen_elements.UITexture import UITexture
from src.render.sprites.BasicSprite import BasicSprite
from src.utils.Loaders import load_texture

import src.render.particle.ParticleShow as ParticleShow


def no_game(_):
    print("No game found.")


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

        self.title_animator = UIAnimatableWidget(
            anchor_x="center",
            anchor_y="top",
            align_y=-50,
            child=UITexture(
                texture=load_texture("assets/pic/Logo.png"),
                scale=7,
            ),
            animator_type=FloatingAnimator,
            animator_params={"speed": 1.0, "phase": 0.4},
        )

        play_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Play/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Play/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Play/pressed.png"),
            scale=8
        )
        play_button.on_click = self.go_game_selector

        credits_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Credits/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Credits/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Credits/pressed.png"),
            scale=8
        )
        credits_button.on_click = self.go_credits

        exit_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Exit/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Exit/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Exit/pressed.png"),
            scale=8
        )
        exit_button.on_click = lambda event: self.core_instance.stop()

        setting_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Settings/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Settings/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Settings/pressed.png"),
            scale=7
        )
        setting_button.on_click = self.go_settings

        self.button_animator = UIAnimatableWidget(
            anchor_x="center",
            anchor_y="bottom",
            align_y=75,
            relative_x=True,
            child=arcade.gui.UIBoxLayout(
                children=[play_button, credits_button, exit_button],
                space_between=15,
            ),
            animator_type=FloatingAnimator,
            animator_params={"speed": 1.0},
        )

        main_screen_layout = UIFullScreenLayout(
            children=[
                self.title_animator,
                self.button_animator,
                arcade.gui.UIAnchorWidget(
                    child=setting_button,
                    anchor_x="right",
                    anchor_y="bottom",
                    align_y=75,
                    align_x=-75,
                ),
            ]
        )

        ###
        # Credits
        ###

        credits_texture = UITexture(
            texture=load_texture("assets/pic/extra/textured_plane.png"),
            scale=8,
        )
        credits_text = arcade.gui.UIBoxLayout(
            space_between=20,
            children=[
                UISuperText(
                    text="CREDITS",
                    width=credits_texture.width - 100,
                    font_size=40,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Alexander Serkov\n"
                         "-----------------------------------\n"
                         "|         Game Physics        |\n"
                         "=> |  Game Design / Visuals  | <=\n"
                         "| Concepts | Code design |\n"
                         "-----------------------------------",
                    width=credits_texture.width - 100,
                    multiline=True,
                    font_size=32,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Artem Batygin\n"
                         "-----------------------------------\n"
                         "=> | Game AI | Game Interfaces | <=\n"
                         "-----------------------------------",
                    width=credits_texture.width - 100,
                    multiline=True,
                    font_size=32,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Vladimir Zakharov\n"
                         "-----------------------------------\n"
                         "=> | Level design | Game AI | <=\n"
                         "-----------------------------------\n",
                    width=credits_texture.width - 100,
                    multiline=True,
                    font_size=32,
                    align="center",
                    bold=True,
                ),
                UISuperText(
                    text="Made with infinite ♥",
                    width=credits_texture.width - 100,
                    text_color=arcade.color.WHITE,
                    font_size=32,
                    align="center",
                ),
            ]
        )
        credits_texture.add(arcade.gui.UIAnchorWidget(
            child=credits_text,
            anchor_x="center",
            anchor_y="top",
            align_y=-30,
        ))

        back_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Arrows/Right/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Arrows/Right/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Arrows/Right/pressed.png"),
            scale=7
        )
        back_button.on_click = self.go_main

        credits_layout = UIFullScreenLayout(
            children=[
                arcade.gui.UIAnchorWidget(
                    child=back_button,
                    anchor_x="right",
                    anchor_y="bottom",
                    align_y=75,
                    align_x=-75,
                ),
                arcade.gui.UIAnchorWidget(
                    child=credits_texture
                ),
            ]
        )

        ###
        # Game Selector
        ###

        back_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Arrows/Left/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Arrows/Left/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Arrows/Left/pressed.png"),
            scale=7
        )
        back_button.on_click = self.go_main

        game_one_button = arcade.gui.UIFlatButton(
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
        game_one_button.on_click = self.start_game

        game_two_button = arcade.gui.UIFlatButton(
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
        game_two_button.on_click = no_game

        game_three_button = arcade.gui.UIFlatButton(
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
        game_three_button.on_click = no_game

        game_selector_layout = UIFullScreenLayout(
            children=[
                arcade.gui.UIAnchorWidget(
                    child=arcade.gui.UIBoxLayout(
                        children=[
                            game_one_button,
                            game_two_button,
                            game_three_button
                        ],
                        space_between=20,
                        vertical=False
                    )
                ),
                arcade.gui.UIAnchorWidget(
                    child=back_button,
                    anchor_x="left",
                    anchor_y="bottom",
                    align_y=75,
                    align_x=75,
                ),
            ]
        )

        ###
        # Settings
        ###

        self.sound_button = arcade.gui.UIFlatButton(
            text="Sound On",
            width=300,
            height=100,
            font_size=30,
            # font_name="Karmatic Arcade",
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.GREEN,
                "hover_font_color": arcade.color.WHITE,
                "hover_bg_color": arcade.color.GREEN,
                "clicked_font_color": arcade.color.WHITE,
                "clicked_bg_color": arcade.color.GREEN,
            }
        )
        self.sound_button.on_click = self.switch_sound

        self.particles_button = arcade.gui.UIFlatButton(
            text="Particles On",
            width=300,
            height=100,
            font_size=30,
            # font_name="Karmatic Arcade",
            style={
                "font_color": arcade.color.WHITE,
                "bg_color": arcade.color.GREEN,
                "hover_font_color": arcade.color.WHITE,
                "hover_bg_color": arcade.color.GREEN,
                "clicked_font_color": arcade.color.WHITE,
                "clicked_bg_color": arcade.color.GREEN,
            }
        )
        self.particles_button.on_click = self.switch_particles

        back_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Arrows/Up/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Arrows/Up/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Arrows/Up/pressed.png"),
            scale=7
        )
        back_button.on_click = self.go_main

        settings_layout = UIFullScreenLayout(
            children=[
                arcade.gui.UIAnchorWidget(
                    child=arcade.gui.UIBoxLayout(
                        children=[
                            self.sound_button,
                            self.particles_button,
                        ],
                        space_between=20,
                    )
                ),
                arcade.gui.UIAnchorWidget(
                    child=back_button,
                    anchor_x="center",
                    anchor_y="top",
                    align_y=-75,
                )
            ]
        )

        ###
        # Screen Layout
        ###

        self.screen_layout = UISuperAnchorWidget(
            anchor_x="center",
            anchor_y="top",
            relative_x=True,
            relative_y=True,
            align_y=-10,
            child=arcade.gui.UIBoxLayout(
                children=[
                    arcade.gui.UIBoxLayout(
                        children=[credits_layout, main_screen_layout, game_selector_layout],
                        vertical=False
                    ),
                    settings_layout
                ]
            ),
        )
        self.manager.add(self.screen_layout)

        self._target_offset_x = 0
        self._target_offset_y = 0

        self._is_sound_on = True
        self._is_particles_on = True

    def update(self, io_controller, delta_time):
        self.background_animator.update(delta_time)

        self.button_animator.update_animation(delta_time)
        self.title_animator.update_animation(delta_time)

        if io_controller.is_key_pressed(arcade.key.ESCAPE) or io_controller.is_key_pressed(arcade.key.BACKSPACE):
            self.go_main(None)

        self.screen_layout.align_x += (self._target_offset_x - self.screen_layout.align_x) * 0.05
        self.screen_layout.align_y += (self._target_offset_y - self.screen_layout.align_y) * 0.05

    def draw(self):
        self.background.draw()

        self.manager.draw()

    def start_game(self, _):
        self.core_instance.set_scene(GameScene)

    def go_credits(self, _):
        self._target_offset_x = 1
        self._target_offset_y = 0

    def go_main(self, _):
        self._target_offset_x = 0
        self._target_offset_y = 0

    def go_game_selector(self, _):
        self._target_offset_x = -1
        self._target_offset_y = 0

    def go_settings(self, _):
        self._target_offset_x = 0
        self._target_offset_y = 1

    def switch_sound(self, _):
        self._is_sound_on = not self._is_sound_on
        self.sound_button.text = "Sound On" if self._is_sound_on else "Sound Off"
        self.sound_button._style = {
            "font_color": arcade.color.WHITE,
            "bg_color": arcade.color.GREEN if self._is_sound_on else arcade.color.RED,
            "hover_font_color": arcade.color.WHITE,
            "hover_bg_color": arcade.color.GREEN if self._is_sound_on else arcade.color.RED,
            "clicked_font_color": arcade.color.WHITE,
            "clicked_bg_color": arcade.color.GREEN if self._is_sound_on else arcade.color.RED,
        }

    def switch_particles(self, _):
        self._is_particles_on = not self._is_particles_on
        ParticleShow.particles_on = self._is_particles_on
        self.particles_button.text = "Particles On" if self._is_particles_on else "Particles Off"
        self.particles_button._style = {
            "font_color": arcade.color.WHITE,
            "bg_color": arcade.color.GREEN if self._is_particles_on else arcade.color.RED,
            "hover_font_color": arcade.color.WHITE,
            "hover_bg_color": arcade.color.GREEN if self._is_particles_on else arcade.color.RED,
            "clicked_font_color": arcade.color.WHITE,
            "clicked_bg_color": arcade.color.GREEN if self._is_particles_on else arcade.color.RED,
        }
