from src.render.sprites.BasicSprite import BasicSprite


class Obstacle:
    def __init__(self, render_group, position, image="../assets/Obstacle.png"):
        self.view = BasicSprite(image, position)
        render_group.add(self.view)