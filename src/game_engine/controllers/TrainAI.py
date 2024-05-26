import arcade
import neat
import os

from src.game_engine.scenes.LearningScene import LearningScene
from src.render.Window import Window, IOController



class Train:
    def __init__(self):
        self.window = Window(1920, 1080, "Train me")
        self.scene = LearningScene()
        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)

        self.pop = None

    def gen(self, genomes, config):
        self.scene.reset()
        self.scene.state = 1

        nets = []
        for i, g in genomes:
            nets.append(neat.nn.FeedForwardNetwork.create(g, config))
            g.fitness = 0

        self.scene.link_models(nets)
        self.scene.link_genomes(genomes)

        print("Scene reset")

    def run(self) -> None:
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            os.path.join(os.path.dirname(__file__), "config.txt")
        )

        self.pop = neat.Population(config)
        stats = neat.StatisticsReporter()
        self.pop.add_reporter(stats)

        self.pop.run(self.gen, 1)
        arcade.run()

        stats.save()
        # print(winner)

    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        self.scene.update(io_controller, delta_time)
        if self.scene.state == 0:
            self.pop.run(self.gen, 1)

    def on_draw(self) -> None:
        self.scene.draw()
