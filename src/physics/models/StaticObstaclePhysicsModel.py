import pymunk


class StaticObstaclePhysicsModel:
    def __init__(
        self, position, shape_type="circle", size=10, collision_points_set=None
    ):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position

        self.shape = None
        if shape_type == "circle":
            self.shape = pymunk.shapes.Circle(self.body, size)
        elif shape_type == "polygon":
            self.shape = pymunk.shapes.Poly(self.body, collision_points_set)
        elif shape_type == "x_barrier":
            self.shape = pymunk.shapes.Segment(
                self.body, (-size / 2, 0), (size / 2, 0), 1
            )
        elif shape_type == "y_barrier":
            self.shape = pymunk.shapes.Segment(
                self.body, (0, -size / 2), (0, size / 2), 1
            )
        self.shape.elasticity = 0.5
        self.shape.friction = 1
        self.shape.collision_type = 30

    def update_position(self, position):
        self.body.position = position

    def update_angle(self, angle):
        self.body.angle = angle
