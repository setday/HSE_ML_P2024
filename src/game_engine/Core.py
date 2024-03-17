import arcade

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.game_engine.scenes.fun_scenes.PhysicScene import PhysicScene
from src.game_engine.scenes.fun_scenes.GameOfLifeScene import GameOfLifeScene
from src.render.Window import Window, IOController


class Core:
    def __init__(self):
        self.window = Window(1920, 1080, "Park me")

        self.scene = GameScene()
        # self.scene = PhysicScene()
        # self.scene = GameOfLifeScene()

        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)
        # self.window.set_render_group(self.scene.render_group)

    def run(self) -> None:
        arcade.run()

    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        self.scene.update(io_controller, delta_time)

    def on_draw(self) -> None:
        self.scene.draw()
