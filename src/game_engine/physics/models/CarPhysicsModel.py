import pymunk


class CarPhysicsModel:
    def __init__(self, position):
        self.body = pymunk.Body(1, pymunk.moment_for_box(1, (50, 100)))
        self.body.position = position

        self.shape = pymunk.Poly.create_box(self.body, (50, 100))
        self.shape.elasticity = 0.5
        self.shape.friction = 1

    def apply_friction(self, friction):
        self.body.velocity /= friction

    def update_position(self, position):
        self.body.position = position

    def update_angle(self, angle):
        self.body.angle = angle

    def turn_left(self, angle, hold_brake=False):
        if not self.is_moving_forward():
            angle = -angle

        # at speed 10 1 angle turn
        angle = angle * self.body.velocity.length / 10

        if not hold_brake and self.body.velocity.length < 40:
            self.body.velocity = self.body.velocity.rotated(angle)
        else:
            self.body.velocity = self.body.velocity.rotated(angle / 10)
        self.update_angle(self.body.angle + angle)

    def accelerate(self, force):
        if self.body.velocity.rotated(-self.body.angle).dot((0, -force)) < 0 and self.body.velocity.length > 100:
            return
        self.body.apply_force_at_local_point((0, -force), (0, 0))

    def brake(self):
        velocity_direction = self.body.velocity.normalized().rotated(-self.body.angle)
        stop_force = velocity_direction * -0.75
        self.body.apply_force_at_local_point((stop_force.x, stop_force.y), (0, 0))

    def is_moving_forward(self):
        return self.body.velocity.rotated(-self.body.angle).y < 0
