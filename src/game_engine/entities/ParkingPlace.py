from math import degrees

from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.sprites.BasicRect import BasicRect


class ParkingPlace:
    def __init__(self, render_group, space, position, size):
        self.obstacle_boundary = BasicRect(*size, position)
        self.obstacle_model = ParkingPlacePhysicsModel(position, size)

        render_group.add(self.obstacle_boundary)

        self.space = space
        self.render_group = render_group

        self.obstacle_model.shape.super = self
        self.space.add(self.obstacle_model.body, self.obstacle_model.shape)
