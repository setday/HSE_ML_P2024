import os
import time
import typing

import arcade

from src.utils import load_image


class IOController:
    def __init__(self) -> None:
        self.keyboard: dict = {}
        self.keyboard_clicked: dict = {}
        self.mouse: dict = {}
        self.mouse_clicked: dict = {}

        self.mouse_position: tuple[float, float] = (0, 0)
        self.mouse_delta: tuple[float, float] = (0, 0)

        self.mouse_scroll_delta: tuple[float, float] = (0, 0)

        self.clicked_keyboard = False
        self.clicked_mouse = {}

    def is_key_pressed(self, key: int) -> bool:
        return self.keyboard.get(key, False)

    def is_key_released(self, key: int) -> bool:
        return not self.keyboard.get(key, False)

    def is_key_clicked(self, key: int) -> bool:
        return self.keyboard_clicked.get(key, False)

    def update_key_state(self, key: int, state: bool) -> None:
        if not state:
            self.keyboard_clicked[key] = True
            self.clicked_keyboard = True
        self.keyboard[key] = state

    def is_mouse_pressed(self, button: int) -> bool:
        return self.mouse.get(button, False)

    def is_mouse_released(self, button: int) -> bool:
        return not self.mouse.get(button, False)

    def is_mouse_clicked(self, button: int) -> bool:
        return self.mouse_clicked.get(button, False)

    def update_mouse_state(self, button: int, state: bool) -> None:
        if not state:
            self.mouse_clicked[button] = True
            self.clicked_mouse = True
        self.mouse[button] = state

    def reset_click_and_scroll(self) -> None:
        if self.clicked_keyboard:
            for key in self.keyboard:
                self.keyboard_clicked[key] = False
        self.clicked_keyboard = False

        if self.clicked_mouse:
            for key in self.mouse:
                self.mouse_clicked[key] = False
        self.clicked_mouse = False

        self.mouse_scroll_delta = (0, 0)


class Window(arcade.Window):
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)

        self.set_icon(load_image("assets/pic/icon/icon.png"))

        # self.center_window()

        self._update_hook = None
        self._draw_hook = None

        self.background_color: arcade.Color = (90, 150, 225)

        self._controller: IOController = IOController()
        self._controller.keyboard = {}

        self._previous_time = time.time()

    def set_update_hook(self, hook: typing.Callable) -> None:
        self._update_hook = hook

    def set_draw_hook(self, hook: typing.Callable) -> None:
        self._draw_hook = hook

    def on_draw(self) -> None:
        super().on_draw()

        self.clear()

        new_time = time.time()
        delta_time = new_time - self._previous_time
        self._previous_time = new_time

        if self._update_hook is not None:
            self._update_hook(self._controller, delta_time)

        self._controller.reset_click_and_scroll()

        if self._draw_hook is not None:
            self._draw_hook()

    def on_update(self, delta_time: float) -> None:
        super().on_update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._controller.update_key_state(symbol, True)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self._controller.update_key_state(symbol, False)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        self._controller.update_mouse_state(button, True)
        self._controller.mouse_position = (x, y)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        self._controller.update_mouse_state(button, False)
        self._controller.mouse_position = (x, y)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self._controller.mouse_position = (x, y)
        self._controller.mouse_delta = (dx, dy)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        self._controller.mouse_scroll_delta = (scroll_x, scroll_y)
