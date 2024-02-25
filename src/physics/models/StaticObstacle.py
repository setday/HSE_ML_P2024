import pymunk


class StaticObstaclePhysicsModel:
    def __init__(self, position, size):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position

        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 0.5
        self.shape.friction = 1
        self.shape.collision_type = 30

    def update_position(self, position):
        self.body.position = position

    def update_angle(self, angle):
        self.body.angle = angle
