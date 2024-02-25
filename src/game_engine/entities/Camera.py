import arcade


class Camera(arcade.Camera):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def camera_move(self):
        x = self.target.center_x - self.viewport_width / 2
        y = self.target.center_y - self.viewport_height / 2
        self.move_to([x, y])
