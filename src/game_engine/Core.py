import arcade

from src.game_engine.scenes.StartScene import StartScene
from src.render.Window import Window, IOController


class Core:
    def __init__(self):
        self.window = Window(1900, 1000, "Park me")
        arcade.load_font('assets/fnt/Title.ttf')
        arcade.load_font('assets/fnt/ka1.ttf')

        self.scene = None

        self.set_scene(StartScene)

        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)

    def set_scene(self, scene) -> None:
        if scene is None:
            scene = StartScene
        self.scene = scene(self)

    def run(self) -> None:
        arcade.run()

    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        if self.scene is not None:
            self.scene.update(io_controller, delta_time)

    def on_draw(self) -> None:
        if self.scene is not None:
            self.scene.draw()
