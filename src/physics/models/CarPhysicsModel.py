import pymunk
from pymunk import Vec2d


class CarPhysicsModel:
    wheels_offset = [
        (-17, -37),
        (17, -37),
        (-17, 37),
        (17, 37)
    ]

    def __init__(self, position, collision_points_set=None):
        self.body = pymunk.Body(2000, pymunk.moment_for_box(2000, (45, 87)))
        self.body.position = position

        self.shape = None
        if collision_points_set is not None:
            self.shape = pymunk.Poly(self.body, collision_points_set)
        else:
            self.shape = pymunk.Poly.create_box(self.body, (45, 87))
        self.shape.elasticity = 0.5
        self.shape.friction = 1
        self.shape.collision_type = 10

    def apply_friction(self, friction_f=1.02, friction_s=1.06):
        local_velocity = self.body.velocity.rotated(-self.body.angle)
        local_velocity = pymunk.Vec2d(local_velocity.x / friction_s, local_velocity.y / friction_f)
        self.body.velocity = local_velocity.rotated(self.body.angle)
        self.body.angular_velocity /= friction_s * friction_f

    def update_position(self, position):
        self.body.position = position

    def update_angle(self, angle):
        self.body.angle = angle

    def turn_left(self, angle, hold_brake=False):
        if not self.is_moving_forward():
            angle = -angle

        # at speed 10 1 angle turn
        angle_coefficient = self.body.velocity.length / 10
        if not hold_brake:
            angle_coefficient = min(1.0, angle_coefficient)
        angle = angle * min(2.0, angle_coefficient)

        if not hold_brake and self.body.velocity.length < 40:
            self.body.velocity = self.body.velocity.rotated(angle)
        else:
            self.body.velocity = self.body.velocity.rotated(angle / 4)
        self.update_angle(self.body.angle + angle)

    def accelerate(self, force):
        force *= self.body.mass
        is_accel = self.body.velocity.rotated(-self.body.angle).dot((0, -force)) > 0
        if is_accel and self.body.velocity.length > 40:
            return
        self.body.apply_force_at_local_point((0, -force), (0, 0))

    def brake(self):
        if self.body.velocity.get_length_sqrd() < 2:
            self.body.velocity /= 3
            return

        velocity_direction = self.body.velocity.normalized().rotated(-self.body.angle)
        stop_force = velocity_direction * -0.25 * self.body.mass * 9.8
        self.body.apply_force_at_local_point((stop_force.x, stop_force.y), (0, 0))

    def is_moving_forward(self):
        return self.body.velocity.rotated(-self.body.angle).y < 0
