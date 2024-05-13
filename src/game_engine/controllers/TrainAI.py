import arcade
import neat
import os
import asyncio

from src.game_engine.scenes.LearningScene import LearningScene
from src.render.Window import Window, IOController


async def run_neat(pop, gen, iters):
    await pop.run(gen, iters)


async def run_arcade():
    await arcade.run()


class Train:
    def __init__(self):
        self.window = Window(1920, 1080, "Train me")
        self.scene = LearningScene()
        self.window.set_update_hook(self.on_update)
        self.window.set_draw_hook(self.on_draw)


    def run(self) -> None:
        def gen(genomes, config):
            nonlocal self

            while self.scene.state == 1:
                pass

            self.scene.reset()      

            nets = []
            for i, g in genomes:
                nets.append(neat.nn.FeedForwardNetwork.create(g, config))
                g.fitness = 0

            self.scene.link_models(nets)
            self.scene.link_genomes(genomes)

            self.scene.state = 1
            # await asyncio.sleep(0)
            # arcade.run()
            # self.window = Window(1920, 1080, "Train me")
            # self.window.set_update_hook(self.on_update)
            # self.window.set_draw_hook(self.on_draw)

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

        loop = asyncio.get_event_loop()
        task1 = loop.create_task(run_neat(pop, gen, 100))
        task2 = loop.create_task(run_arcade())
        loop.run_until_complete(asyncio.wait([task1, task2]))

        # winner = pop.run(gen, 100)
        stats.save()
        # print(winner)

        
    def on_update(self, io_controller: IOController, delta_time: float) -> None:
        self.scene.update(io_controller, delta_time)

    def on_draw(self) -> None:
        self.scene.draw()
