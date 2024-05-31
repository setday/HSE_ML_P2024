import math

from pyglet.math import Vec2 as Vector2D
from pymunk import Space

from src.physics.models.ParkingPlacePhysicModel import ParkingPlacePhysicsModel
from src.render.scene_elements import RenderGroup
from src.render.sprites import BasicRect


class ParkingPlace:
    def __init__(
        self,
        render_group: RenderGroup,
        space: Space,
        position: Vector2D | tuple[float, float],
        size: tuple[float, float] = (65, 110),
        angle: float = 0,
    ):
        # self.base_view = BasicSprite("assets/parking_place_background.png", position)
        # self.dead_view = BasicSprite("assets/parking_place_face.png", position)
        self.parking_model: ParkingPlacePhysicsModel = ParkingPlacePhysicsModel(
            position, size, angle
        )

        self.border_box: BasicRect = BasicRect(int(size[0]), int(size[1]), position)
        self.border_box.update_angle(math.degrees(angle))
        self.border_box.set_border_width(4)

        # self.border_box_dead_zones = []
        # for i in range(4):
        #     dz = self.parking_model.dead_zones[i]
        #     dz_shape = self.parking_model.dead_zone_shapes[i]
        #     points = dz_shape.get_vertices()
        #     width = points[1][0] - points[3][0]
        #     height = points[1][1] - points[3][1]
        #     print(points)
        #     width = max(width, 4)
        #     height = max(height, 4)
        #     offset = (points[1][0] + points[3][0]) / 2, (points[1][1] + points[3][1]) / 2
        #     self.border_box_dead_zones.append(
        #         BasicRect(math.ceil(width), math.ceil(height), dz.position + offset)
        #     )
        #     self.border_box_dead_zones[i].update_color((255, 0, 0))
        #     self.border_box_dead_zones[i].update_angle(math.degrees(angle))
        #     self.border_box_dead_zones[i].set_border_width(1)

        # self.base_view.update_angle(degrees(angle))
        # self.dead_view.update_angle(degrees(angle))

        # render_group.add(self.base_view)
        # render_group.add(self.dead_view)

        render_group.add(self.border_box)
        # for dz in self.border_box_dead_zones:
        #     render_group.add(dz)

        self.space: Space = space
        self.render_group: RenderGroup = render_group

        self.parking_model.inner_shape.super = self
        for i in range(len(self.parking_model.dead_zones)):
            self.parking_model.dead_zone_shapes[i].super = self
            self.space.add(
                self.parking_model.dead_zones[i], self.parking_model.dead_zone_shapes[i]
            )

        self.space.add(self.parking_model.inner_body, self.parking_model.inner_shape)
