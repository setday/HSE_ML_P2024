from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.sprites.BasicRect import BasicRect


class ParkingPlace:
    def __init__(self, render_group, space, position, size, offset):
        self.base_boundary = BasicRect(*size, position)
        self.dead_boundary = BasicRect(size[0] - offset, size[1] - offset, position)
        self.parking_model = ParkingPlacePhysicsModel(position, size, offset)

        render_group.add(self.base_boundary)
        render_group.add(self.dead_boundary)

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
