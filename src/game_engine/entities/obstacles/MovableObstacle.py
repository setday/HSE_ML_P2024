from math import degrees

from src.physics.models.MovableObstacle import MovableObstaclePhysicsModel
from src.render.sprites.BasicRect import BasicRect
from src.render.sprites.BasicSprite import BasicSprite


class MovableObstacle:
    def __init__(self, render_group, space, position):
        self.obstacle_view = BasicSprite("assets/Traffic_Cone.png", position)
        self.obstacle_boundary = BasicRect(16, 16, position)
        self.obstacle_model = MovableObstaclePhysicsModel(position, (16, 16))

        render_group.add(self.obstacle_view)
        render_group.add(self.obstacle_boundary)

        self.space = space
        self.render_group = render_group

        self.obstacle_model.shape.super = self
        self.space.add(self.obstacle_model.body, self.obstacle_model.shape)
        # self.screen.add_drawable(self.car_view)

        self.health = 100

        self.sync()

    def apply_friction(self):
        self.obstacle_model.apply_friction()

    def sync(self):
        def inverse_y(pos: Vector2D) -> Vector2D:
            return Vector2D(pos.x, -pos.y)

        self.obstacle_view.update_position(inverse_y(self.obstacle_model.body.position))
        self.obstacle_view.update_angle(-degrees(self.obstacle_model.body.angle))

        self.obstacle_boundary.update_position(inverse_y(self.obstacle_model.body.position))
        self.obstacle_boundary.update_angle(-degrees(self.obstacle_model.body.angle))

    def turn_debug_view(self, mode=True):
        pass
