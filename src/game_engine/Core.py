import arcade

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.Window import Window


class Core:
    def __init__(self):
        self.window = Window(800, 800, "Park me")

        self.scene = GameScene()

        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)
        # self.window.set_render_group(self.scene.render_group)

    def run(self):
        arcade.run()

    def on_update(self, keys, delta_time):
        self.scene.update(keys, delta_time)

    def on_draw(self):
        self.scene.draw()
