import pygame

from src.render.RenderGroup import RenderGroup


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.__screen = pygame.display.set_mode((width, height))
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))

        pygame.display.set_caption("Park Me")

        self.__render_group = None

    def get_screen(self):
        return self.__screen

    def set_render_group(self, render_group: RenderGroup) -> None:
        """
        @summary Sets the render group to draw
        @param render_group: The render group to draw
        """
        self.__render_group = render_group

    def draw_frame(self):
        self.__screen.fill((255, 0, 0))

        if self.__render_group is not None:
            self.__render_group.update()
            self.__render_group.custom_draw(self.__screen)

        pygame.display.update()
