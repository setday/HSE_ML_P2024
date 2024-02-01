import pygame

from src.render.RenderGroup import RenderGroup


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__screen = pygame.display.set_mode((width, height))
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))

        pygame.display.set_caption("Park Me")

        self.__render_group = None

    def set_render_group(self, render_group):
        self.__render_group = render_group

    def draw_frame(self):
        self.__screen.fill((255, 0, 0))

        if self.__render_group is not None:
            self.__render_group.update()
            self.__render_group.custom_draw(self.__screen)

        pygame.display.update()
