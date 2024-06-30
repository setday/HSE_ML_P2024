from typing import Any

import arcade
from pyglet.math import Vec2 as Vector2D  # type: ignore[import-untyped]

from src.render.sprites import BasicSprite


class Indicator:
    def __init__(
        self,
        owner: Any,
        position: Vector2D | tuple[float, float] = (300, 300),
        width: int = 200,
        height: int = 21,
        border_size: int = 5,
        icon: str = "assets/pic/icon/heart_2.png",
        score_color: arcade.Color = (161, 256, 111),
        trail_color: arcade.Color = (255, 184, 84),
        background_color: arcade.Color = (135, 135, 135),
        border_color: arcade.Color = (56, 56, 56),
    ) -> None:
        self.sprite_list = arcade.SpriteList()

        self.owner = None
        if hasattr(owner, "health") and isinstance(owner.health, int):
            self.owner = owner
        else:
            raise ValueError(
                f"Invalid owner type: {type(owner)} has no health attribute"
            )

        self.target_health: int = 0
        self.current_health: int = 0

        self.box_width: int = width
        self.box_height: int = height
        self.half_box_width: int = self.box_width // 2
        self.border_width: int = border_size

        self.center_x: float = 0.0
        self.center_y: float = 0.0

        self.change_speed: float = 0.03
        self.position: tuple[float, float] = (0, 0)

        self.border_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width + self.border_width * 2,
            self.box_height + self.border_width * 2,
            border_color,
        )
        self.background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            background_color,
        )

        self.trail_shadow_box_1: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            border_color,
        )
        self.trail_shadow_box_2: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width + self.border_width * 2,
            self.box_height - self.border_width * 2,
            border_color,
        )

        self.trail_box_1: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            trail_color,
        )
        self.trail_box_2: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width + self.half_box_width,
            self.box_height - self.border_width * 2,
            trail_color,
        )

        self.score_box_1: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width,
            self.box_height,
            score_color,
        )
        self.score_box_2: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.box_width + self.half_box_width,
            self.box_height - self.border_width * 2,
            score_color,
        )

        self.update_bar()

        self.icon: BasicSprite = BasicSprite(icon, scale=5.5)
        self.icon.position = (-self.half_box_width, 0)

        self.sprite_list.append(self.border_box)
        self.sprite_list.append(self.background_box)
        self.sprite_list.append(self.trail_shadow_box_1)
        self.sprite_list.append(self.trail_shadow_box_2)
        self.sprite_list.append(self.trail_box_1)
        self.sprite_list.append(self.trail_box_2)
        self.sprite_list.append(self.score_box_1)
        self.sprite_list.append(self.score_box_2)
        self.sprite_list.append(self.icon)

        self.set_position(position)

    def _set_score_box(self, new_width: int) -> None:
        self.score_box_1.width = new_width
        self.score_box_2.width = new_width + self.border_width
        self.score_box_2.left = self.score_box_1.left = (
            self.center_x - self.half_box_width
        )

    def _set_trail_box(self, new_width: int) -> None:
        self.trail_box_1.width = new_width
        self.trail_box_2.width = new_width + self.border_width
        self.trail_box_2.left = self.trail_box_1.left = (
            self.center_x - self.half_box_width
        )

        self.trail_shadow_box_1.width = new_width + self.border_width
        self.trail_shadow_box_2.width = new_width + self.border_width * 2
        self.trail_shadow_box_2.left = self.trail_shadow_box_1.left = (
            self.center_x - self.half_box_width
        )

    def _set_target_health(self, new_health: int) -> None:
        self.target_health = new_health

        if self.target_health < self.current_health:
            self._set_score_box(self.target_health)
        else:
            self._set_trail_box(self.target_health)

    def _update_current_health(self) -> None:
        self.current_health -= (
            self.current_health - self.target_health
        ) * self.change_speed
        if abs(self.current_health - self.target_health) < 1:
            self.current_health = self.target_health

        if self.current_health < self.target_health:
            self._set_score_box(self.current_health)
        else:
            self._set_trail_box(self.current_health)

    def update_bar(self) -> None:
        new_health = max(0.001, self.owner.health)

        if new_health * 2 != self.target_health:
            self._set_target_health(int(2 * new_health))

        if self.current_health != self.target_health:
            self._update_current_health()

    def set_position(self, new_position: Vector2D | tuple[float, float]) -> None:
        if new_position != self.position:
            new_x, new_y = new_position
            delta_x: float = new_x - self.center_x
            delta_y: float = new_y - self.center_y
            self.position = new_position
            self.center_x, self.center_y = new_position
            self.sprite_list.move(delta_x, delta_y)
