import pygame

from src.game_engine.scenes.GameScene import GameScene
from src.render.Window import Window


class Core:
    def __init__(self):
        pygame.init()

        self.window = Window(800, 800)
        self.scene = GameScene(self.window)
        self.window.set_render_group(self.scene.render_group)

        self.is_running = False

    def stop(self):
        self.is_running = False

    def run(self):
        self.is_running = True

        self.update_loop()

    def update_loop(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()

    def update(self):
        self.scene.update()

    def draw(self):
        self.scene.draw()

        self.window.draw_frame()
