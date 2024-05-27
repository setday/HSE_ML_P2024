from arcade.color import RED, GREEN, WHITE
from arcade.gui import UIFlatButton, UITextureButton, UIAnchorWidget, UIBoxLayout

from src.utils.Loaders import load_texture

from src.render.screen_elements.ui_components.UIFullScreenLayout import UIFullScreenLayout

import src.render.particle.ParticleShow as ParticleShow


_is_sound_on = True
_is_particles_on = True


class SettingLayout(UIFullScreenLayout):
    def __init__(self, back_callback: callable):
        ###
        # Settings
        ###

        self.sound_button = UIFlatButton(
            text="",
            width=300,
            height=100,
            font_size=30,
            # font_name="Karmatic Arcade",
        )
        self.sound_button.on_click = self.switch_sound

        self.particles_button = UIFlatButton(
            text="",
            width=300,
            height=100,
            font_size=30,
            # font_name="Karmatic Arcade",
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
                            self.sound_button,
                            self.particles_button,
                        ],
                        space_between=20,
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

    def switch_sound(self, _):
        global _is_sound_on
        _is_sound_on = not _is_sound_on

        self.redraw_buttons()

    def switch_particles(self, _):
        global _is_particles_on
        _is_particles_on = not _is_particles_on
        ParticleShow.particles_on = _is_particles_on

        self.redraw_buttons()

    def redraw_buttons(self):
        global _is_sound_on, _is_particles_on

        self.sound_button.text = "Sound On" if _is_sound_on else "Sound Off"
        self.sound_button._style = {
            "font_color": WHITE,
            "bg_color": GREEN if _is_sound_on else RED,
            "hover_font_color": WHITE,
            "hover_bg_color": GREEN if _is_sound_on else RED,
            "clicked_font_color": WHITE,
            "clicked_bg_color": GREEN if _is_sound_on else RED,
        }

        self.particles_button.text = "Particles On" if _is_particles_on else "Particles Off"
        self.particles_button._style = {
            "font_color": WHITE,
            "bg_color": GREEN if _is_particles_on else RED,
            "hover_font_color": WHITE,
            "hover_bg_color": GREEN if _is_particles_on else RED,
            "clicked_font_color": WHITE,
            "clicked_bg_color": GREEN if _is_particles_on else RED,
        }
