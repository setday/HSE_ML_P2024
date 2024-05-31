import time

import arcade

from src.game_engine.scenes import StartScene
from src.render.Window import Window, IOController
from src.utils import load_font


class Core:
    def __init__(self):
        self.window = Window(1920, 1080, "Park me")

        load_font("assets/fnt/Title.ttf")
        load_font("assets/fnt/ka1.ttf")

        self.scene = None

        self.is_active: bool = False

        self.set_scene(StartScene)

        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)

        if not arcade.timings_enabled():
            arcade.enable_timings()

    def set_scene(self, scene) -> None:
        if scene is None:
            scene = StartScene
        self.scene = scene(self)
        self.scene.init_music_player(self.window)

    def run(self) -> None:
        self.is_active = True

        arcade.run()

    def stop(self) -> None:
        self.is_active = False

        arcade.exit()

    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        self.window.set_caption("Park me" + " " + f"FPS: {round(arcade.get_fps(), 2)}")

        if io_controller.is_key_clicked(arcade.key.F6):
            image = arcade.get_image()
            image.save(f"data/screenshots/{time.time()}.png")

        if self.scene is not None:
            self.scene.update(io_controller, delta_time)

    def on_draw(self) -> None:
        if self.scene is not None:
            self.scene.draw()
