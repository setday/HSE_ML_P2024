import pymunk


class MovableObstaclePhysicsModel:
    def __init__(self, position, size=(10, 10)):
        self.body = pymunk.Body(5, pymunk.moment_for_box(5, size))
        self.body.position = position

        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 0.5
        self.shape.friction = 1
        self.shape.collision_type = 20

    def apply_friction(self, friction=1.02):
        local_velocity = self.body.velocity.rotated(-self.body.angle)
        local_velocity = pymunk.Vec2d(local_velocity.x / (friction * friction), local_velocity.y / friction)
        self.body.velocity = local_velocity.rotated(self.body.angle)
        self.body.angular_velocity /= friction * friction

    def update_position(self, position):
        self.body.position = position

    def update_angle(self, angle):
        self.body.angle = angle
