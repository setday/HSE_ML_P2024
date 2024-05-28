from arcade.gui import UITextureButton, UIBoxLayout, UIAnchorWidget, UIManager
from arcade.key import ESCAPE, BACKSPACE

from src.game_engine.scenes.layouts.SettingLayout import SettingLayout
from src.render.screen_elements.ui_components.UIFullScreenLayout import UIFullScreenLayout
from src.render.screen_elements.ui_components.UISuperAnchorWidget import UISuperAnchorWidget
from src.render.screen_elements.ui_components.UITexture import UITexture
from src.utils.Loaders import load_texture


class EscapeMenuLayout:
    def __init__(self, close_callback: callable, home_callback: callable):
        ###
        # EscapeMenu
        ###

        self.manager = UIManager()
        self.manager.enable()

        self.title = UIAnchorWidget(
            anchor_x="center",
            anchor_y="top",
            align_y=-50,
            child=UITexture(
                texture=load_texture("assets/pic/boards/Pause.png"),
                scale=7,
            ),
        )

        back_button = UITextureButton(
            texture=load_texture("assets/pic/buttons/Close/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Close/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Close/pressed.png"),
            scale=7
        )
        back_button.on_click = close_callback

        setting_button = UITextureButton(
            texture=load_texture("assets/pic/buttons/Settings/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Settings/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Settings/pressed.png"),
            scale=7
        )
        setting_button.on_click = self.go_settings

        home_button = UITextureButton(
            texture=load_texture("assets/pic/buttons/Home/normal.png"),
            texture_hovered=load_texture("assets/pic/buttons/Home/hovered.png"),
            texture_pressed=load_texture("assets/pic/buttons/Home/pressed.png"),
            scale=7
        )
        home_button.on_click = home_callback

        buttons_layout = UIBoxLayout(
            space_between=20,
            children=[
                back_button,
                setting_button,
                home_button,
            ]
        )

        buttons_wrapper = UIAnchorWidget(
            anchor_x="left",
            anchor_y="center",
            align_x=10,
            child=buttons_layout
        )

        self.screen_layout = UISuperAnchorWidget(
            anchor_x="center",
            anchor_y="top",
            relative_x=True,
            relative_y=True,
            child=UIBoxLayout(
                children=[
                    UIFullScreenLayout(
                        children=[buttons_wrapper]
                    ),
                    SettingLayout(self.go_selector),
                ]
            )
        )
        self.manager.add(self.screen_layout)

        self.close_callback = close_callback

        self._target_offset_x = -0.1
        self._target_offset_y = 0

    def update(self, io_controller, delta_time):
        if io_controller.is_key_clicked(ESCAPE) or io_controller.is_key_clicked(BACKSPACE):
            self.close_callback(None)

        delta_translation = delta_time / 16 * 50
        delta_translation = min(delta_translation, 0.5)

        self.screen_layout.align_x += (self._target_offset_x - self.screen_layout.align_x) * delta_translation
        self.screen_layout.align_y += (self._target_offset_y - self.screen_layout.align_y) * delta_translation

    def draw(self):
        self.manager.draw()

    def go_selector(self, _):
        self._target_offset_x = 0
        self._target_offset_y = 0

    def go_settings(self, _):
        self._target_offset_x = 0
        self._target_offset_y = 1

    def hide(self):
        self._target_offset_x = -0.1
        self._target_offset_y = 0

    def show(self):
        self.go_selector(None)
