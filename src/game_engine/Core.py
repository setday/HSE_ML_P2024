import arcade

from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.game_engine.scenes.game_scene.StartScene import StartScene
from src.game_engine.scenes.fun_scenes.PhysicScene import PhysicScene
from src.game_engine.scenes.fun_scenes.GameOfLifeScene import GameOfLifeScene
from src.render.Window import Window, IOController


class Core:
    def __init__(self):
        self.window = Window(1920, 1080, "Park me")
        arcade.load_font('assets/Title.ttf')
        self.scene = StartScene()
        # self.scene = PhysicScene()
        # self.scene = GameOfLifeScene()

        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)
        # self.window.set_render_group(self.scene.render_group)

    def run(self) -> None:
        arcade.run()

    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        if isinstance(self.scene, GameScene):
            self.scene.update(io_controller, delta_time)
        elif isinstance(self.scene, StartScene):
            if self.scene.game_started:
                self.scene = GameScene()
        else:
            pass

    def on_draw(self) -> None:
        self.scene.draw()
