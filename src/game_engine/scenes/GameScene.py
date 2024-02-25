import arcade
import pymunk


class GameScene(arcade.Scene):
    def __init__(self, window, image='../assets/Map2.jpg'):
        super().__init__()
        self.window = window
        self.cnt = 0
        self.space = pymunk.Space()
        h = self.space.add_collision_handler(0, 0)
        h.begin = self.collision_detecter
        self.background = arcade.load_texture(image)

    def collision_detecter(arbiter, space, data):
        print('Bah')
        return True
