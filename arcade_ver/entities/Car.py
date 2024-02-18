import arcade
import math
# import sys
# sys.path.append(r"../assets")
import Consts


class Car(arcade.Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.turning = 0.0

    def car_move(self, delta_time):
        self.angle += Consts.TURN_SPEED_DEGREES * self.turning * delta_time
        x_dir = math.cos(self.radians - math.pi / 2)
        y_dir = math.sin(self.radians - math.pi / 2)
        self.position = self.center_x + x_dir, self.center_y + y_dir
