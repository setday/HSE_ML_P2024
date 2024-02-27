import arcade

from src.render.Camera import Camera


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background_color = arcade.color.AMAZON

        self.camera = Camera()

        self.keyboard = {}

    def on_draw(self):
        super().on_draw()

        self.clear()
        # arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height, self.scene.background)

    def on_update(self, delta_time):
        super().on_update(delta_time)

    def on_key_press(self, symbol, modifiers):
        self.keyboard[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.keyboard[symbol] = False
