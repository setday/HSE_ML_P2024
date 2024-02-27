import arcade


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self._update_hook = None
        self._draw_hook = None

        self.background_color = arcade.color.AMAZON

        self._keyboard = {}

    def set_update_hook(self, hook):
        self._update_hook = hook

    def set_draw_hook(self, hook):
        self._draw_hook = hook

    def on_draw(self):
        super().on_draw()

        self.clear()

        if self._draw_hook is not None:
            self._draw_hook()

    def on_update(self, delta_time):
        super().on_update(delta_time)

        if self._update_hook is not None:
            self._update_hook(self._keyboard, delta_time)

    def on_key_press(self, symbol, modifiers):
        self._keyboard[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self._keyboard[symbol] = False
