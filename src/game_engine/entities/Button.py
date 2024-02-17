import pygame


class Button:
    def __init__(self,
                 width=50,
                 height=30,
                 active_color=(52, 50, 158),
                 inactive_color=(191, 190, 250),
                 msg='add'):
        self.wight = width
        self.height = height
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.size = height - 10
        self.msg = pygame.font.SysFont('arial', size=self.size).render(msg, self.size, (0, 0, 0))

    def draw(self, x, y, action, screen):
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + self.wight and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.wight, self.height))
            if pygame.mouse.get_pressed()[0]:
                for elem in pygame.event.get():
                    if elem.type == pygame.MOUSEBUTTONUP:
                        action(5)
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.wight, self.height))
        screen.blit(self.msg, (y - 5, x))
