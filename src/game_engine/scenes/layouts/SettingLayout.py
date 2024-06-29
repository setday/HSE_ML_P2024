from arcade.gui import UITextureButton, UIAnchorWidget, UIBoxLayout

from src.game_engine.entities.MusicPlayer import set_sound_level, get_sound_level
from src.render.particle import change_particles_state, get_particles_state
from src.render.screen_elements.ui_components import (
    UICheckButton,
    UIFullScreenLayout,
    UISlider,
)
from src.utils import load_texture

_is_particles_on = True


class SettingLayout(UIFullScreenLayout):
    def __init__(self, back_callback: callable):
        self._sound_level = int(get_sound_level() * 10)

        ###
        # Settings
        ###

        self.sound_button = UICheckButton(
            textures_checked=(
                load_texture("assets/pic/buttons/Sound/normal_on.png"),
                load_texture("assets/pic/buttons/Sound/hovered_on.png"),
                load_texture("assets/pic/buttons/Sound/pressed_on.png"),
            ),
            textures_unchecked=(
                load_texture("assets/pic/buttons/Sound/normal_off.png"),
                load_texture("assets/pic/buttons/Sound/hovered_off.png"),
                load_texture("assets/pic/buttons/Sound/pressed_off.png"),
            ),
            scale=6,
            checked=(self._sound_level != 0),
            on_change=lambda _: self.set_sound_level(),
        )

        self.sound_slider = UISlider(
            textures=(
                load_texture("assets/pic/slider/Slider_1_10.png"),
                load_texture("assets/pic/slider/Slider_2_10.png"),
                load_texture("assets/pic/slider/Slider_3_10.png"),
                load_texture("assets/pic/slider/Slider_4_10.png"),
                load_texture("assets/pic/slider/Slider_5_10.png"),
                load_texture("assets/pic/slider/Slider_6_10.png"),
                load_texture("assets/pic/slider/Slider_7_10.png"),
                load_texture("assets/pic/slider/Slider_8_10.png"),
                load_texture("assets/pic/slider/Slider_9_10.png"),
                load_texture("assets/pic/slider/Slider_10_10.png"),
            ),
            scale=5,
            change_callback=self.set_sound_level,
        )

        self.particles_button = UICheckButton(
            textures_checked=(
                load_texture("assets/pic/buttons/Effects/normal_on.png"),
                load_texture("assets/pic/buttons/Effects/hovered_on.png"),
                load_texture("assets/pic/buttons/Effects/pressed_on.png"),
            ),
            textures_unchecked=(
                load_texture("assets/pic/buttons/Effects/normal_off.png"),
                load_texture("assets/pic/buttons/Effects/hovered_off.png"),
                load_texture("assets/pic/buttons/Effects/pressed_off.png"),
            ),
            scale=6,
            checked=(self._sound_level != 0),
            on_change=self.switch_particles,
        )

        self.redraw_buttons()

        back_button = UITextureButton(
            texture=load_texture("assets/pic/buttons/Arrows/Up/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Arrows/Up/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Arrows/Up/pressed.png"),
            scale=7,
        )
        back_button.on_click = back_callback

        super().__init__(
            children=[
                UIAnchorWidget(
                    child=UIBoxLayout(
                        children=[
                            UIBoxLayout(
                                children=[
                                    self.sound_slider,
                                    self.sound_button,
                                ],
                                space_between=-202,
                            ),
                            self.particles_button,
                        ],
                        space_between=150,
                    )
                ),
                UIAnchorWidget(
                    child=back_button,
                    anchor_x="center",
                    anchor_y="top",
                    align_y=-75,
                ),
            ]
        )

        global _is_particles_on
        _is_particles_on = get_particles_state()

    def set_sound_level(self, level: float | None = None):
        if not level:
            self._sound_level = 0 if self._sound_level else 9
        else:
            self._sound_level = level

        self.redraw_buttons()

        set_sound_level(self._sound_level / 10)

    def switch_particles(self, state: bool):
        global _is_particles_on
        _is_particles_on = state
        change_particles_state(_is_particles_on)

        self.redraw_buttons()

    def redraw_buttons(self):
        self.sound_button.switch_state(self._sound_level != 0)
        self.sound_slider.value = self._sound_level
