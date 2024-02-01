import pygame


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, image, position, group):
        super().__init__(group)

        self.src_image = pygame.image.load(image)
        self.image = self.src_image

        self.rect = self.src_image.get_rect()
        self.rect.center = position

        self.angle = 0
        self.position = position

    def update_position(self, position):
        self.rect.center = self.position = position

    def update_angle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.src_image, self.angle)
        self.rect = self.image.get_rect(center=self.position)
