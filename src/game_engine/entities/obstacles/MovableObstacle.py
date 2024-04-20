from math import degrees

from pymunk import Space
from pyglet.math import Vec2 as Vector2D

from src.physics.models.MovableObstacle import MovableObstaclePhysicsModel
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite


class MovableObstacle:
    def __init__(self,
                 render_group: RenderGroup,
                 space: Space,
                 position: Vector2D = (0, 0),
                 angle: float = 0,
                 image_path: str = "assets/pic/obstacles/Traffic_Cone.png"):
        self.obstacle_view = BasicSprite(image_path, position)

        x, y = position

        self.obstacle_model = MovableObstaclePhysicsModel((x, y), self.obstacle_view.get_hit_box())
        self.obstacle_model.body.angle = angle

        render_group.add(self.obstacle_view)

        self.space = space
        self.render_group = render_group

        self.obstacle_model.shape.super = self
        self.space.add(self.obstacle_model.body, self.obstacle_model.shape)

        self.health = 100

        self.sync()

    def apply_friction(self):
        self.obstacle_model.apply_friction()

    def sync(self):
        self.obstacle_view.update_position(self.obstacle_model.body.position)
        self.obstacle_view.update_angle(degrees(self.obstacle_model.body.angle))

    def turn_debug_view(self, mode=True):
        pass

    def remove(self):
        self.obstacle_view.remove_from_sprite_lists()
        self.space.remove(self.obstacle_model.body, self.obstacle_model.shape)
