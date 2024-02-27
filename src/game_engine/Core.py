import arcade

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.Window import Window


class Core(Window):
    def __init__(self):
        super().__init__(800, 800, "Park me")

        # self.window = Window(800, 800)
        self.scene = GameScene(self)
        # self.window.set_render_group(self.scene.render_group)

    def on_update(self, delta_time):
        super().on_update(delta_time)

        self.scene.update(self.keyboard, delta_time)

    def on_draw(self):
        super().on_draw()

        self.scene.draw()
