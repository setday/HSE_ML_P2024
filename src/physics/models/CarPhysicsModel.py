import pymunk
from pymunk import Vec2d


class CarPhysicsModel:
    wheels_offset: list[tuple[float, float]] = [
        (-17, -37),
        (17, -37),
        (-17, 37),
        (17, 37),
    ]

    def __init__(
        self, position: Vec2d | tuple[float, float], collision_points_set=None
    ) -> None:
        self.body: pymunk.Body = pymunk.Body(
            2000, pymunk.moment_for_box(2000, (45, 87))
        )
        self.body.position = position

        self.shape: pymunk.Poly | None = None

        if collision_points_set is not None:
            self.shape = pymunk.Poly(self.body, collision_points_set)
        else:
            self.shape = pymunk.Poly.create_box(self.body, (45, 87))
        self.shape.elasticity = 0.5
        self.shape.friction = 1
        self.shape.collision_type = 10

    def apply_friction(
        self, friction_f: float = 1.02, friction_s: float = 1.06
    ) -> None:
        local_velocity: Vec2d = self.body.velocity.rotated(-self.body.angle)
        local_velocity = pymunk.Vec2d(
            local_velocity.x / friction_s, local_velocity.y / friction_f
        )
        self.body.velocity = local_velocity.rotated(self.body.angle)
        self.body.angular_velocity /= friction_s * friction_f

    def update_position(self, position: Vec2d | tuple[float, float]) -> None:
        self.body.position = position

    def update_angle(self, angle: float) -> None:
        self.body.angle = angle

    def turn_left(self, angle: float, hold_brake: bool = False) -> None:
        if not self.is_moving_forward():
            angle = -angle

        # at speed 10 1 angle turn
        angle_coefficient: float = self.body.velocity.length / 10
        if not hold_brake:
            angle_coefficient = min(1.0, angle_coefficient)
        angle = angle * min(2.0, angle_coefficient)

        if not hold_brake and self.body.velocity.length < 40:
            self.body.velocity = self.body.velocity.rotated(angle)
        else:
            self.body.velocity = self.body.velocity.rotated(angle / 4)
        self.update_angle(self.body.angle + angle)

    def accelerate(self, force: float) -> None:
        force *= self.body.mass
        is_accel: bool = (
            self.body.velocity.rotated(-self.body.angle).dot((0, -force)) > 0
        )
        if is_accel and self.body.velocity.length > 40:
            return
        self.body.apply_force_at_local_point((0, -force), (0, 0))

    def brake(self) -> None:
        if self.body.velocity.get_length_sqrd() < 2:
            self.body.velocity /= 3
            return

        velocity_direction: Vec2d = self.body.velocity.normalized().rotated(
            -self.body.angle
        )
        stop_force: Vec2d = velocity_direction * -0.25 * self.body.mass * 9.8
        self.body.apply_force_at_local_point((stop_force.x, stop_force.y), (0, 0))

    def is_moving_forward(self) -> bool:
        return self.body.velocity.rotated(-self.body.angle).y < 0
