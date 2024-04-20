from math import degrees

from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.sprites.BasicSprite import BasicSprite


class ParkingPlace:
    def __init__(self, render_group, space, position, size, offset, angle):
        self.base_view = BasicSprite("assets/parking_place_background.png", position)
        self.dead_view = BasicSprite("assets/parking_place_face.png", position)
        self.parking_model = ParkingPlacePhysicsModel(position, size, offset, angle)

        self.base_view.update_angle(degrees(angle))
        self.dead_view.update_angle(degrees(angle))

        render_group.add(self.base_view)
        render_group.add(self.dead_view)

        self.space = space
        self.render_group = render_group

        self.parking_model.inner_shape.super = self
        for i in range(len(self.parking_model.dead_zones)):
            self.parking_model.dead_zone_shapes[i].super = self
            self.space.add(self.parking_model.dead_zones[i], self.parking_model.dead_zone_shapes[i])

        self.space.add(self.parking_model.inner_body, self.parking_model.inner_shape)
