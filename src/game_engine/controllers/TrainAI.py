import arcade

from src.game_engine.scenes.LearningScene import LearningScene
from src.render.Window import Window, IOController


class Train:
    def __init__(self):
        self.window = Window(1920, 1080, "Train me")
        self.scene = LearningScene()
        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)

    def run(self) -> None:
        for i in range(10 ** 2):
            self.scene.reset()            
            # костыль:
            try:
                arcade.run()
            except Exception as exc:
                print(type(exc))
                print(exc.args)
                print(exc)

            print(f"Epoch #{i + 1} ended with result: {self.scene.get_score()}")


    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        self.scene.update(io_controller, delta_time)

    def on_draw(self) -> None:
        self.scene.draw()
