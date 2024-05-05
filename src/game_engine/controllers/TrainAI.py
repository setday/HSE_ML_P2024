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


    def run(self) -> None:
        def gen(genomes, config):
            nonlocal self

            self.scene.reset()            

            nets = []
            for i, g in genomes:
                nets.append(neat.nn.FeedForwardNetwork.create(g, config))
                g.fitness = 0

            self.scene.link_models(nets)
            self.scene.link_genomes(genomes)
            self.scene.set_tick_lim(100)

            arcade.run()
            self.window = Window(1920, 1080, "Train me")
            self.window.set_update_hook(self.on_update)
            self.window.set_draw_hook(self.on_draw)

        config = neat.config.Config(
            neat.DefaultGenome, 
            neat.DefaultReproduction, 
            neat.DefaultSpeciesSet, 
            neat.DefaultStagnation, 
            os.path.join(os.path.dirname(__file__), "config.txt")
        )
        pop = neat.Population(config)
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        winner = pop.run(gen, 10)
        stats.save()
        print(winner)

        
    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        self.scene.update(io_controller, delta_time)

    def on_draw(self) -> None:
        self.scene.draw()
