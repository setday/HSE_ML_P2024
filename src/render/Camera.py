import arcade
from pyglet.math import Vec2 as Vector2D


class Camera(arcade.Camera):
    def __init__(self):
        super().__init__()

        self._screen_shift = Vector2D(self.viewport_width / 2, self.viewport_height / 2)

        self._target_position = -self._screen_shift
        self._target_zoom = 1

        self._snapped_sprite = None

    def snap_to_sprite(self, sprite) -> None:
        self._snapped_sprite = sprite

    def set_position(self, position: Vector2D) -> None:
        self._target_position = position

    def get_position(self, vertical_state: int = 0, horizontal_state: int = 0) -> Vector2D:
        """
        Returns the position of the camera.
        vertical_state: -1 for top, 0 for middle, 1 for bottom.
        horizontal_state: -1 for left, 0 for middle, 1 for right.
        """

        vertical_offset = (1 + vertical_state) * self.viewport_height / 2
        horizontal_offset = (1 + horizontal_state) * self.viewport_width / 2

        return self.position + Vector2D(horizontal_offset, vertical_offset)

    def set_zoom(self, zoom: float) -> None:
        self._target_zoom = zoom

    def get_zoom(self) -> float:
        return self._target_zoom

    def update(self):
        if self._snapped_sprite is not None:
            x, y = self._snapped_sprite.position
            self.set_position(Vector2D(x, y))

        self.scale += (self._target_zoom - self.scale) * 0.05

        self.move_to(self._target_position - self._screen_shift, 0.05)

        super().update()
