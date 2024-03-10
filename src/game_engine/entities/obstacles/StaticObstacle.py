from math import degrees

from src.physics.models.StaticObstacle import StaticObstaclePhysicsModel
from src.render.sprites.BasicSprite import BasicSprite


class StaticObstacle:
    def __init__(self, render_group, space, position):
        self.obstacle_view = BasicSprite("assets/pic/Tree_1.png", position)
        self.obstacle_model = StaticObstaclePhysicsModel(position, (20, 20))

        render_group.add(self.obstacle_view)

        self.space = space
        self.render_group = render_group

        self.obstacle_model.shape.super = self
        self.space.add(self.obstacle_model.body, self.obstacle_model.shape)

        self.sync()

    def sync(self):
        self.obstacle_view.update_position(self.obstacle_model.body.position)
        self.obstacle_view.update_angle(degrees(self.obstacle_model.body.angle))

    def turn_debug_view(self, mode=True):
        pass
