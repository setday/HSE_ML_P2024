from arcade.color import RED, GREEN, WHITE
from arcade.gui import UIFlatButton, UITextureButton, UIAnchorWidget, UIBoxLayout

import src.render.particle.ParticleShow as ParticleShow
from src.render.screen_elements.ui_components.UICheckButton import UICheckButton
from src.render.screen_elements.ui_components.UIFullScreenLayout import UIFullScreenLayout
from src.render.screen_elements.ui_components.UISlider import UISlider
from src.utils.Loaders import load_texture

_sound_level = 4
_is_particles_on = True


class SettingLayout(UIFullScreenLayout):
    def __init__(self, back_callback: callable):
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
            checked=_sound_level != 0,
            on_change=lambda _: self.set_sound_level()
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

        self.particles_button = UIFlatButton(
            text="",
            width=300,
            height=100,
            font_size=30,
        )
        self.particles_button.on_click = self.switch_particles

        self.redraw_buttons()

        back_button = UITextureButton(
            texture=load_texture("assets/pic/buttons/Arrows/Up/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Arrows/Up/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Arrows/Up/pressed.png"),
            scale=7
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
                )
            ]
        )

        global _is_particles_on
        _is_particles_on = ParticleShow.particles_on

    def set_sound_level(self, level: float | None = None):
        global _sound_level
        if not level:
            _sound_level = 0 if _sound_level else 4
        else:
            _sound_level = level

        self.redraw_buttons()

    def switch_particles(self, _):
        global _is_particles_on
        _is_particles_on = not _is_particles_on
        ParticleShow.particles_on = _is_particles_on

        self.redraw_buttons()

    def redraw_buttons(self):
        global _sound_level, _is_particles_on

        self.sound_button.switch_state(_sound_level != 0)
        self.sound_slider.value = _sound_level

        self.particles_button.text = "Particles On" if _is_particles_on else "Particles Off"
        self.particles_button._style = {
            "font_color": WHITE,
            "bg_color": GREEN if _is_particles_on else RED,
            "hover_font_color": WHITE,
            "hover_bg_color": GREEN if _is_particles_on else RED,
            "clicked_font_color": WHITE,
            "clicked_bg_color": GREEN if _is_particles_on else RED,
        }
