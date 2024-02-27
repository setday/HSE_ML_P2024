from math import degrees

from pymunk import Vec2d as Vector2D

from src.physics.models.StaticObstacle import StaticObstaclePhysicsModel
from src.render.sprites.BasicRect import BasicRect
from src.render.sprites.BasicSprite import BasicSprite


class StaticObstacle:
    def __init__(self, render_group, space, position):
        self.obstacle_view = BasicSprite("assets/Tree_1.png", position)
        self.obstacle_boundary = BasicRect(20, 20, position)
        self.obstacle_model = StaticObstaclePhysicsModel(position, (20, 20))

        render_group.add(self.obstacle_view)
        render_group.add(self.obstacle_boundary)

        self.space = space
        self.render_group = render_group

        self.obstacle_model.shape.super = self
        self.space.add(self.obstacle_model.body, self.obstacle_model.shape)

        self.sync()

    def sync(self):
        def inverse_y(pos: Vector2D) -> Vector2D:
            return Vector2D(pos.x, -pos.y)

        self.obstacle_view.update_position(inverse_y(self.obstacle_model.body.position))
        self.obstacle_view.update_angle(-degrees(self.obstacle_model.body.angle))

        self.obstacle_boundary.update_position(inverse_y(self.obstacle_model.body.position))
        self.obstacle_boundary.update_angle(-degrees(self.obstacle_model.body.angle))

    def turn_debug_view(self, mode=True):
        pass
