import pymunk


class ParkingPlacePhysicsModel:
    def __init__(self, position, size, margin):
        self.inner_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.inner_body.position = position

        self.outer_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.outer_body.position = position

        self.inner_shape = pymunk.Poly.create_box(self.inner_body, size)
        # self.inner_shape.elasticity = 0.5
        # self.inner_shape.friction = 1
        self.inner_shape.collision_type = 41

        self.outer_shape = pymunk.Poly.create_box(self.outer_body, (size[0] + margin, size[1] + margin))
        # self.outer_shape.elasticity = 0.5
        # self.outer_shape.friction = 1
        self.outer_shape.collision_type = 42

    def update_position(self, position):
        self.inner_body.position = position

    def update_angle(self, angle):
        self.inner_body.angle = angle
