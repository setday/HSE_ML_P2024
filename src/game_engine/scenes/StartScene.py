import arcade
import arcade.gui

from src.game_engine.scenes.game_scene.modes.A2BScene import A2BScene
from src.game_engine.scenes.game_scene.modes.ParkMeScene import ParkMeScene
from src.game_engine.scenes.game_scene.modes.SurvivalScene import SurvivalScene
from src.render.animator import FloatingAnimator, WanderAnimator
from src.render.screen_elements.effect_animator import EffectAnimator, FadeEffect
from src.render.screen_elements.ui_components import (
    UIFullScreenLayout,
    UIAnimatableWidget,
    UISuperAnchorWidget,
    UITexture,
)
from src.utils import load_texture
from .layouts import CreditsLayout, SettingLayout


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

        self.background_animator = UIAnimatableWidget(
            anchor_x="center",
            anchor_y="bottom",
            child=UITexture(
                texture=load_texture("assets/pic/extra/Clouds.png"), scale=15
            ),
            animator_type=WanderAnimator,
            animator_params={
                "limits_x": (-3000, 3000),
                "limits_y": (0, 0),
                "speed": 0.02,
            },
        )

        self.manager.add(self.background_animator)

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
            scale=8,
        )
        play_button.on_click = self.go_game_selector

        credits_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Credits/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Credits/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Credits/pressed.png"),
            scale=8,
        )
        credits_button.on_click = self.go_credits

        exit_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Exit/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Exit/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Exit/pressed.png"),
            scale=8,
        )
        exit_button.on_click = lambda event: self.core_instance.stop()

        setting_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Settings/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Settings/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Settings/pressed.png"),
            scale=7,
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

        credits_layout = CreditsLayout(self.go_main)

        ###
        # Game Selector
        ###

        game_selector_title = arcade.gui.UIAnchorWidget(
            anchor_x="center",
            anchor_y="top",
            align_y=-50,
            child=UITexture(
                texture=load_texture("assets/pic/boards/Games.png"),
                scale=7,
            ),
        )

        back_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/Arrows/Left/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Arrows/Left/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Arrows/Left/pressed.png"),
            scale=7,
        )
        back_button.on_click = self.go_main

        game_one_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/GameSelection/PMS/normal.png"),
            texture_hovered=load_texture(
                "assets/pic/buttons/GameSelection/PMS/hovered.png"
            ),
            texture_pressed=load_texture(
                "assets/pic/buttons/GameSelection/PMS/pressed.png"
            ),
        )
        game_one_button.on_click = lambda _: self.start_game(self, "park")

        game_two_button = arcade.gui.UITextureButton(
            texture=load_texture(
                "assets/pic/buttons/GameSelection/Survival/normal.png"
            ),
            texture_hovered=load_texture(
                "assets/pic/buttons/GameSelection/Survival/hovered.png"
            ),
            texture_pressed=load_texture(
                "assets/pic/buttons/GameSelection/Survival/pressed.png"
            ),
        )
        game_two_button.on_click = lambda _: self.start_game(self, "survive")

        game_three_button = arcade.gui.UITextureButton(
            texture=load_texture("assets/pic/buttons/GameSelection/A2B/normal.png"),
            texture_hovered=load_texture(
                "assets/pic/buttons/GameSelection/A2B/hovered.png"
            ),
            texture_pressed=load_texture(
                "assets/pic/buttons/GameSelection/A2B/pressed.png"
            ),
        )
        game_three_button.on_click = lambda _: self.start_game(self, "a2b")

        game_selector_layout = UIFullScreenLayout(
            children=[
                arcade.gui.UIAnchorWidget(
                    child=arcade.gui.UIBoxLayout(
                        children=[game_one_button, game_two_button, game_three_button],
                        space_between=20,
                        vertical=False,
                    )
                ),
                arcade.gui.UIAnchorWidget(
                    child=back_button,
                    anchor_x="left",
                    anchor_y="bottom",
                    align_y=75,
                    align_x=75,
                ),
                game_selector_title,
            ]
        )

        ###
        # Settings
        ###

        settings_layout = SettingLayout(self.go_main)

        ###
        # Screen Layout
        ###

        self.screen_layout = UISuperAnchorWidget(
            anchor_x="center",
            anchor_y="top",
            relative_x=True,
            relative_y=True,
            align_y=-1,
            child=arcade.gui.UIBoxLayout(
                children=[
                    arcade.gui.UIBoxLayout(
                        children=[
                            credits_layout,
                            main_screen_layout,
                            game_selector_layout,
                        ],
                        vertical=False,
                    ),
                    settings_layout,
                ]
            ),
        )
        self.manager.add(self.screen_layout)

        self._target_offset_x = 0
        self._target_offset_y = -1

        self._effect_animator = EffectAnimator()
        self._effect_animator.add_effect(
            FadeEffect(
                duration=1,
                delay=0.5,
                fade_color=(255, 255, 255),
                fade_in=False,
                finish_callback=lambda: self.go_main(None),
            )
        )

        self.core_instance.music_manager.change_track_list(
            ["assets/sounds/music/lobby.mp3"], loop=True
        )

        self.is_destroyed = False

    def do_destroy(self):
        self.manager.disable()
        del self.manager

        del self.background_animator
        del self.title_animator
        del self.button_animator
        del self.screen_layout
        del self._effect_animator

        self.is_destroyed = True

    def update(self, io_controller, delta_time):
        if self.is_destroyed:
            raise Exception("This scene has been destroyed.")

        self.background_animator.update_animation(delta_time)

        self.button_animator.update_animation(delta_time)
        self.title_animator.update_animation(delta_time)

        if io_controller.is_key_clicked(
            arcade.key.ESCAPE
        ) or io_controller.is_key_clicked(arcade.key.BACKSPACE):
            self.go_main(None)

        delta_translation = delta_time / 16 * 50
        delta_translation = min(delta_translation, 0.5)

        self.screen_layout.align_x += (
            self._target_offset_x - self.screen_layout.align_x
        ) * delta_translation
        self.screen_layout.align_y += (
            self._target_offset_y - self.screen_layout.align_y
        ) * delta_translation

        self._effect_animator.update(delta_time)

    def draw(self):
        if self.is_destroyed:
            raise Exception("This scene has been destroyed.")

        self.manager.draw()

        self._effect_animator.draw()

    def start_game(self, _, mode: str):
        if self.is_destroyed:
            raise Exception("This scene has been destroyed.")

        scene: type[ParkMeScene] | type[SurvivalScene] | type[A2BScene] | None = None

        if mode == "park":
            scene = ParkMeScene
        elif mode == "survive":
            scene = SurvivalScene
        elif mode == "a2b":
            scene = A2BScene

        self._effect_animator.add_effect(
            FadeEffect(
                duration=1,
                fade_color=(255, 255, 255),
                finish_callback=lambda: self.core_instance.set_scene(scene),
            )
        )

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
