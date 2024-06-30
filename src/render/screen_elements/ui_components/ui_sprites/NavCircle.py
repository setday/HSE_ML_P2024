from typing import Any

import arcade
from pyglet.math import Vec2 as Vector2D

from src.render.sprites import BasicSprite

from src.utils import ObjBunch, PositionalClass


class NavCircleArrow(BasicSprite):
    def __init__(
        self,
        target: PositionalClass,
        center_position: Vector2D | tuple[float, float],
        radius: float,
        color: tuple[int, int, int] = arcade.color.WHITE,
        unvanishable: bool = False,
    ) -> None:
        self._target = target
        self._center_position = center_position
        self._radius = radius

        self._radius_sqrt = radius * radius

        super().__init__("assets/pic/extra/arrow.png")

        self.color = color

        self._life_timer = 1.0
        self._is_disappearing = False

        self._unvanishable = unvanishable

    def _get_dist(self) -> float:
        x1, y1 = self._target.position
        x2, y2 = self._center_position
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def _get_arrow_radius(self) -> float:
        return self._radius * (1 - 1 / (1 + self._get_dist() / self._radius_sqrt))

    def _get_arrow_angle(self) -> float:
        x1, y1 = self._target.position
        x2, y2 = self._center_position
        direction = Vector2D(y1 - y2, x1 - x2)
        return direction.heading

    def _get_arrow_position(self) -> Vector2D:
        return Vector2D(0, -self._get_arrow_radius()).rotate(self._get_arrow_angle())

    def _get_arrow_opacity(self) -> float:
        dist_factor = (self._get_dist() / 9.0 / self._radius_sqrt) ** 2

        if self._unvanishable:
            dist_factor = min(3.0, dist_factor)

        if dist_factor > 150.0:
            return 0.0
        if dist_factor <= 1.0:
            return 255.0

        return 255.0 / dist_factor

    def is_dead(self) -> bool:
        return self._life_timer <= 0

    def update_arrow(self, delta_time: float) -> None:
        if self.is_dead():
            return
        if self._is_disappearing:
            self.alpha /= self._life_timer
            self._life_timer = max(0.0, self._life_timer - delta_time)
            self.alpha *= self._life_timer
            return

        self.update_angle(self._get_arrow_angle() * 180 / 3.141592653589793)
        self.update_position(self._get_arrow_position())

        self.alpha = self._get_arrow_opacity() * 0.8

    def kill(self):
        self._is_disappearing = True


class NavCircle:
    def __init__(
        self,
        owner: PositionalClass | tuple[float, float] | Vector2D | None = None,
        radius: float = 300,
    ) -> None:
        self.sprite_list = arcade.SpriteList()

        if owner is None:
            owner = Vector2D(0, 0)
        if isinstance(owner, tuple) or isinstance(owner, Vector2D):
            owner = ObjBunch(position=owner)
        self._owner = owner

        self._virtual_position = self._owner.position

        self._owner = owner
        self._radius = radius

    def add_target(
        self,
        owner: Vector2D | tuple[float, float] | PositionalClass,
        target_type: str = "unknown",
        unvanishable: bool = False,
    ) -> NavCircleArrow:
        type_colors = {
            "unknown": arcade.color.WHITE,
            "enemy": arcade.color.ORANGE_RED,
            "ally": arcade.color.LIGHT_GREEN,
            "parking_place": arcade.color.LIGHT_BLUE,
        }

        if target_type not in type_colors:
            raise ValueError(f"NavCircleArrow target type {target_type} is not valid")

        if isinstance(owner, Vector2D) or isinstance(owner, tuple):
            owner = ObjBunch(position=owner)

        arrow = NavCircleArrow(
            owner,
            self._virtual_position,
            self._radius,
            type_colors[target_type],
            unvanishable,
        )
        self.sprite_list.append(arrow)

        return arrow

    def update(self, delta_time: float) -> None:
        to_remove = []

        self._virtual_position.x, self._virtual_position.y = self._owner.position

        for sprite in self.sprite_list:
            if isinstance(sprite, NavCircleArrow):
                if sprite.is_dead():
                    to_remove.append(sprite)
                sprite.update_arrow(delta_time)

        for sprite in to_remove:
            self.sprite_list.remove(sprite)
