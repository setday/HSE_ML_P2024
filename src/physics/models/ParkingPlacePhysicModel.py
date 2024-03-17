import pymunk


class ParkingPlacePhysicsModel:
    def __init__(self, position, size, offset):
        self.inner_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.inner_body.position = position

        self.outer_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.outer_body.position = position

        self.dead_zones = [
            pymunk.Body(body_type=pymunk.Body.STATIC),
            pymunk.Body(body_type=pymunk.Body.STATIC),
            pymunk.Body(body_type=pymunk.Body.STATIC),
            pymunk.Body(body_type=pymunk.Body.STATIC)
        ]

        self.dead_zones[0].position = (position[0] - size[0] / 2 + offset / 2, position[1])
        self.dead_zones[1].position = (position[0] + size[0] / 2 - offset / 2, position[1])
        self.dead_zones[2].position = (position[0], position[1] + size[1] / 2 - offset / 2)
        self.dead_zones[3].position = (position[0], position[1] - size[1] / 2 + offset / 2)

        self.inner_shape = pymunk.Poly.create_box(self.inner_body, size)
        self.inner_shape.collision_type = 40

        self.dead_zone_shapes = [
            pymunk.Poly.create_box(self.dead_zones[0], (offset, size[0])),
            pymunk.Poly.create_box(self.dead_zones[1], (offset, size[0])),
            pymunk.Poly.create_box(self.dead_zones[2], (size[1], offset)),
            pymunk.Poly.create_box(self.dead_zones[3], (size[1], offset))
        ]

        for zone in self.dead_zone_shapes:
            zone.collision_type = 41
