from math import degrees

from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.sprites.BasicRect import BasicRect

from pyglet.math import Vec2


class ParkingPlace:
    def __init__(self, render_group, space, position, size, margin):
        self.base_boundary = BasicRect(*size, position)
        self.dead_boundary = BasicRect(size[0] - margin, size[1] - margin, position)
        self.parking_model = ParkingPlacePhysicsModel(position, size, margin)

        render_group.add(self.base_boundary)
        render_group.add(self.dead_boundary)

        self.tr1 = 0
        self.tr2 = 0

        # self.preview = [
        #     BasicRect(margin, size[1], Vec2(position[0] - size[0] / 2 + margin / 2, position[1])),
        #     BasicRect(margin, size[1], Vec2(position[0] + size[0] / 2 - margin / 2, position[1])),
        #     BasicRect(size[0], margin, Vec2(position[0], position[1] + size[1] / 2 - margin / 2)),
        #     BasicRect(size[0], margin, Vec2(position[0], position[1] - size[1] / 2 + margin / 2))
        # ]
        #
        # for _ in self.preview:
        #     render_group.add(_)

        self.space = space
        self.render_group = render_group

        self.parking_model.inner_shape.super = self
        for i in range(len(self.parking_model.dead_zones)):
            self.parking_model.dead_zone_shapes[i].super = self
            self.space.add(self.parking_model.dead_zones[i], self.parking_model.dead_zone_shapes[i])

        self.space.add(self.parking_model.inner_body, self.parking_model.inner_shape)
