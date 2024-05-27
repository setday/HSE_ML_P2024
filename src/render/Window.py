import arcade

from src.utils.Loaders import load_image


class IOController:
    def __init__(self):
        self.keyboard = {}
        self.mouse = {}

        self.keyboard_clicked = {}

        self.mouse_position = (0, 0)
        self.mouse_delta = (0, 0)

        self.clicked = False

    def is_key_pressed(self, key: int) -> bool:
        return self.keyboard.get(key, False)

    def is_key_released(self, key: int) -> bool:
        return not self.keyboard.get(key, False)

    def is_key_clicked(self, key: int) -> bool:
        return self.keyboard_clicked.get(key, False)

    def update_key_state(self, key: int, state: bool) -> None:
        if not state:
            self.keyboard_clicked[key] = True
            self.clicked = True
        self.keyboard[key] = state

    def reset_click(self) -> None:
        if self.clicked:
            for key in self.keyboard:
                self.keyboard_clicked[key] = False
        self.clicked = False


class Window(arcade.Window):
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)

        self.set_icon(load_image("assets/pic/icon/icon.png"))

        # self.center_window()

        self._update_hook = None
        self._draw_hook = None

        self.background_color = (90, 150, 225)

        self._controller = IOController()
        self._controller.keyboard = {}

    def set_update_hook(self, hook: callable) -> None:
        self._update_hook = hook

    def set_draw_hook(self, hook: callable) -> None:
        self._draw_hook = hook

    def on_draw(self) -> None:
        super().on_draw()

        self.clear()

        if self._draw_hook is not None:
            self._draw_hook()

    def on_update(self, delta_time: float) -> None:
        super().on_update(delta_time)

        if self._update_hook is not None:
            self._update_hook(self._controller, delta_time)

        self._controller.reset_click()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._controller.update_key_state(symbol, True)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self._controller.update_key_state(symbol, False)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        self._controller.mouse[button] = True
        self._controller.mouse_position = (x, y)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        self._controller.mouse[button] = False
        self._controller.mouse_position = (x, y)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self._controller.mouse_position = (x, y)
        self._controller.mouse_delta = (dx, dy)
