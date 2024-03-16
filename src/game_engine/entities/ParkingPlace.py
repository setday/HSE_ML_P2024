from math import degrees

from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.sprites.BasicRect import BasicRect


class ParkingPlace:
    def __init__(self, render_group, space, position, size, margin):
        self.inner_obstacle_boundary = BasicRect(*size, position)
        self.outer_obstacle_boundary = BasicRect(size[0] + margin, size[1] + margin, position)
        self.obstacle_model = ParkingPlacePhysicsModel(position, size, margin)

        render_group.add(self.inner_obstacle_boundary)
        render_group.add(self.outer_obstacle_boundary)

        self.space = space
        self.render_group = render_group

        self.obstacle_model.inner_shape.super = self
        self.obstacle_model.outer_shape.super = self
        self.space.add(self.obstacle_model.inner_body, self.obstacle_model.inner_shape)
        self.space.add(self.obstacle_model.outer_body, self.obstacle_model.outer_shape)
