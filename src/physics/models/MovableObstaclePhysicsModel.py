import pymunk


class MovableObstaclePhysicsModel:
    def __init__(self, position, collision_points_set=None):
        self.body = pymunk.Body(5, pymunk.moment_for_box(5, (16, 16)))
        self.body.position = position

        self.shape = None
        if collision_points_set is not None:
            self.shape = pymunk.Poly(self.body, collision_points_set)
        else:
            self.shape = pymunk.Poly.create_box(self.body, (16, 16))
        self.shape.elasticity = 0.5
        self.shape.friction = 1
        self.shape.collision_type = 20

    def apply_friction(self, friction=1.02):
        self.body.velocity = self.body.velocity / friction / friction
        self.body.angular_velocity /= friction * friction

    def update_position(self, position):
        self.body.position = position

    def update_angle(self, angle):
        self.body.angle = angle
