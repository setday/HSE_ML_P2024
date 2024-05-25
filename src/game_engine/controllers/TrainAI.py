import arcade
import neat
import os

from neat.six_util import iteritems

from src.game_engine.scenes.LearningScene import LearningScene
from src.render.Window import Window, IOController


class Train:
    def __init__(self, view_mode=False, spectate_mode=False):
        self.view_mode = view_mode
        if self.view_mode:
            self.window = Window(1920, 1080, "Train me (view mode)")
        else:
            self.window = Window(100, 100, "Train me")
        self.scene = LearningScene(self.view_mode, spectate_mode)
        self.window.set_update_rate(1 / 10000)
        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)

        self.pop = None

    def update_scene_genomes(self, genomes, config):
        self.scene.reset()
        self.scene.state = 1

        nets = []
        for i, g in genomes:
            nets.append(neat.nn.FeedForwardNetwork.create(g, config))
            g.fitness = 0

        self.scene.link_models(nets)
        self.scene.link_genomes(genomes)

    def run(self) -> None:
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            os.path.join(os.path.dirname(__file__), "config.txt"),
        )

        self.pop = neat.Population(config)
        stats = neat.StatisticsReporter()
        self.pop.add_reporter(stats)

        self.update_scene_genomes(list(iteritems(self.pop.population)), self.pop.config)
        arcade.run()

        stats.save()

    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        self.scene.update(io_controller, delta_time)

        if self.scene.state == 0:
            self.scene.update_cars_fitness()
            self.pop.run(lambda a, b: None, 1)
            self.update_scene_genomes(
                list(iteritems(self.pop.population)), self.pop.config
            )

    def on_draw(self) -> None:
        if self.view_mode:
            self.scene.draw()
