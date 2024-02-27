import arcade
import pyglet
from pyglet.math import Vec2


class Camera(arcade.Camera):
    def __init__(self):
        super().__init__()

        self.real_position = pyglet.math.Vec2(0, 0)
        self.zoom = 1

        self.target_position = pyglet.math.Vec2(0, 0)
        self.target_zoom = 1

        self.screen_shift = pyglet.math.Vec2(self.viewport_width / 2, self.viewport_height / 2)

        self.snapped_sprite = None

    def snap_to_sprite(self, sprite) -> None:
        self.snapped_sprite = sprite

    def set_position(self, position: pyglet.math.Vec2) -> None:
        self.target_position = position

    def set_zoom(self, zoom: float) -> None:
        self.target_zoom = zoom

        # for sprite in self.sprites():
        #     sprite.update_scale(zoom)

    def update(self):
        if self.snapped_sprite is not None:
            x, y = self.snapped_sprite.position
            self.set_position(pyglet.math.Vec2(x, y))

        self.real_position += (self.target_position - self.real_position) * Vec2(0.03, 0.03)
        self.zoom += (self.target_zoom - self.zoom) * 0.003

        self.move(self.real_position - self.screen_shift)
        
        super().update()
