import pygame.image

from src.render.sprites.BasicSprite import BasicSprite


class ParkingPlace:
    def __init__(self, render_group,  position, image='../assets/FreePark.png'):
        self.view = BasicSprite(image, position)
        render_group.add(self.view)
        self.IsBusy = False

    def change_view(self):
        if self.IsBusy:
            self.view.image = pygame.image.load('../assets/FreePark.png')
            self.IsBusy = False
        else:
            self.view.image = pygame.image.load('../assets/BusyPark.png')
            self.IsBusy = True