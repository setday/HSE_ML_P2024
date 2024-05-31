from math import degrees

from pyglet.math import Vec2 as Vector2D
from pymunk import Space

from src.physics.models.MovableObstaclePhysicsModel import MovableObstaclePhysicsModel
from src.render.scene_elements import RenderGroup
from src.render.sprites import BasicSprite


class MovableObstacle:
    def __init__(
        self,
        render_group: RenderGroup,
        space: Space,
        position: Vector2D = (0, 0),
        angle: float = 0,
        image_path: str = "assets/pic/obstacles/Traffic_Cone.png",
    ) -> None:
        self.obstacle_view: BasicSprite = BasicSprite(image_path, position)

        x, y = position

        self.obstacle_model: MovableObstaclePhysicsModel = MovableObstaclePhysicsModel(
            (x, y), self.obstacle_view.get_hit_box()
        )
        self.obstacle_model.body.angle = angle

        render_group.add(self.obstacle_view)

        self.space: Space = space
        self.render_group: RenderGroup = render_group

        self.obstacle_model.shape.super = self
        self.space.add(self.obstacle_model.body, self.obstacle_model.shape)

        self.health: int = 100

        self.sync()

    def apply_friction(self) -> None:
        self.obstacle_model.apply_friction()

    def sync(self) -> None:
        self.obstacle_view.update_position(self.obstacle_model.body.position)
        self.obstacle_view.update_angle(degrees(self.obstacle_model.body.angle))

    def turn_debug_view(self, mode: bool = True) -> None:
        pass

    def remove(self) -> None:
        self.obstacle_view.remove_from_sprite_lists()
        self.space.remove(self.obstacle_model.body, self.obstacle_model.shape)
