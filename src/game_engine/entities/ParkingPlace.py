from math import degrees

from pyglet.math import Vec2 as Vector2D
from pymunk import Space

from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.RenderGroup import RenderGroup
from src.render.sprites.BasicRect import BasicRect
from src.render.sprites.BasicSprite import BasicSprite


class ParkingPlace:
    def __init__(self,
                 render_group: RenderGroup,
                 space: Space,
                 position: Vector2D | tuple[float, float],
                 size: tuple[float, float] = (65, 110),
                 angle: float = 0):
        # self.base_view = BasicSprite("assets/parking_place_background.png", position)
        # self.dead_view = BasicSprite("assets/parking_place_face.png", position)
        self.parking_model = ParkingPlacePhysicsModel(position, size, angle)

        self.border_box = BasicRect(int(size[0]), int(size[1]), position)
        self.border_box.update_angle(degrees(angle))
        self.border_box.set_border_width(4)

        # self.base_view.update_angle(degrees(angle))
        # self.dead_view.update_angle(degrees(angle))

        # render_group.add(self.base_view)
        # render_group.add(self.dead_view)

        render_group.add(self.border_box)

        self.space = space
        self.render_group = render_group

        self.parking_model.inner_shape.super = self
        for i in range(len(self.parking_model.dead_zones)):
            self.parking_model.dead_zone_shapes[i].super = self
            self.space.add(self.parking_model.dead_zones[i], self.parking_model.dead_zone_shapes[i])

        self.space.add(self.parking_model.inner_body, self.parking_model.inner_shape)
