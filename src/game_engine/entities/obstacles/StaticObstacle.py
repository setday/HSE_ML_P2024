from math import degrees

from pyglet.math import Vec2 as Vector2D
from pymunk import Space

from src.physics.models.StaticObstaclePhysicsModel import StaticObstaclePhysicsModel
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicSprite import BasicSprite


class StaticObstacle:
    def __init__(
        self,
        render_group: RenderGroup,
        space: Space,
        position: Vector2D = (0, 0),
        angle: float = 0,
        image_path: str | None = "assets/pic/obstacles/Tree_1.png",
        shape_type: str = None,
    ) -> None:
        self.obstacle_view: BasicSprite | None = None
        if image_path is not None:
            self.obstacle_view = BasicSprite(image_path, position)

        x, y = position

        shape_size: int = 20000
        if shape_type == "circle":
            shape_size: int = 10

        if shape_type != "self":
            self.obstacle_model = StaticObstaclePhysicsModel(
                (x, y), shape_type, shape_size
            )
        else:
            self.obstacle_model = StaticObstaclePhysicsModel(
                (x, y), "polygon", 0, self.obstacle_view.get_hit_box()
            )
        self.obstacle_model.body.angle = angle

        if self.obstacle_view is not None:
            render_group.add(self.obstacle_view)

        self.space: Space = space
        self.render_group: RenderGroup = render_group

        self.obstacle_model.shape.super = self
        self.space.add(self.obstacle_model.body, self.obstacle_model.shape)

        self.sync()

    def sync(self) -> None:
        if self.obstacle_view is None:
            return

        self.obstacle_view.update_position(self.obstacle_model.body.position)
        self.obstacle_view.update_angle(degrees(self.obstacle_model.body.angle))

    def turn_debug_view(self, mode: bool = True) -> None:
        pass
