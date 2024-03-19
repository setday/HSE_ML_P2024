from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.sprites.BasicRect import BasicRect
from src.render.sprites.BasicSprite import BasicSprite

from math import degrees


class ParkingPlace:
    def __init__(self, render_group, space, position, size, offset, angle):
        self.base_view = BasicSprite("assets/parking_place_background.png", position)
        self.dead_view = BasicSprite("assets/parking_place_face.png", position)
        self.parking_model = ParkingPlacePhysicsModel(position, size, offset, angle)

        self.base_view.update_angle(degrees(angle))
        self.dead_view.update_angle(degrees(angle))

        render_group.add(self.base_view)
        render_group.add(self.dead_view)

        self.update_color((255, 0, 0))

        self.space = space
        self.render_group = render_group

        self.parking_model.inner_shape.super = self
        for i in range(len(self.parking_model.dead_zones)):
            self.parking_model.dead_zone_shapes[i].super = self
            self.space.add(self.parking_model.dead_zones[i], self.parking_model.dead_zone_shapes[i])

        self.space.add(self.parking_model.inner_body, self.parking_model.inner_shape)

    def update_color(self, color):
        self.base_boundary.update_color(color)
        self.dead_boundary.update_color(color)
