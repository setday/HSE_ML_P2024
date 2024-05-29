import pymunk


def create_box_with_offset(body: pymunk.Body, size: tuple[float, float], offset: tuple[float, float]) -> pymunk.Poly:
    vert: list[tuple[float, float]] = [
        (size[0] / 2 + offset[0], -size[1] / 2 + offset[1]),
        (size[0] / 2 + offset[0], size[1] / 2 + offset[1]),
        (-size[0] / 2 + offset[0], size[1] / 2 + offset[1]),
        (-size[0] / 2 + offset[0], -size[1] / 2 + offset[1]),
    ]

    return pymunk.Poly(body, vert)


class ParkingPlacePhysicsModel:
    def __init__(
        self,
        position: tuple[float, float],
        size: tuple[float, float] = (70, 120),
        angle: float = 0,
    ) -> None:
        self.inner_body: pymunk.Body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.inner_body.position = position
        self.inner_body.angle = angle

        self.inner_shape: pymunk.Poly = pymunk.Poly.create_box(self.inner_body, size)
        self.inner_shape.collision_type = 40

        self.outer_body: pymunk.Body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.outer_body.position = position
        self.outer_body.angle = angle

        self.dead_zones: list[pymunk.Body] = [
            pymunk.Body(body_type=pymunk.Body.STATIC),
            pymunk.Body(body_type=pymunk.Body.STATIC),
            pymunk.Body(body_type=pymunk.Body.STATIC),
            pymunk.Body(body_type=pymunk.Body.STATIC),
        ]

        dead_zone_width: int = 2

        self.dead_zones[0].position = position
        self.dead_zones[1].position = position
        self.dead_zones[2].position = position
        self.dead_zones[3].position = position

        self.dead_zones[0].angle = angle
        self.dead_zones[1].angle = angle
        self.dead_zones[2].angle = angle
        self.dead_zones[3].angle = angle

        self.dead_zone_shapes: list[pymunk.Poly] = [
            create_box_with_offset(self.dead_zones[0], (dead_zone_width, size[1]), (-size[0] / 2, 0)),
            create_box_with_offset(self.dead_zones[1], (dead_zone_width, size[1]), (size[0] / 2, 0)),
            create_box_with_offset(self.dead_zones[2], (size[0], dead_zone_width), (0, size[1] / 2)),
            create_box_with_offset(self.dead_zones[3], (size[0], dead_zone_width), (0, -size[1] / 2)),
        ]

        for zone in self.dead_zone_shapes:
            zone.collision_type = 41
