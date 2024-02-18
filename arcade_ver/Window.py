import arcade
import Consts
from entities.Car import Car
import math
from entities.Camera import Camera


class Window(arcade.Window):
    def __init__(self, width, height, title, image='assets/Map2.jpg'):
        super().__init__(width, height, title)
        self.background = arcade.load_texture(image)
        self.car = Car('assets/car_2.png')
        self.sprites = arcade.SpriteList()
        self.sprites.append(self.car)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=0.4)
        self.physics_engine.add_sprite(self.car, friction=Consts.FRICTION, mass=Consts.MASS)
        self.camera = Camera(self.car)
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(1024, 1024, 2048, 2048, self.background)
        self.camera.use()
        self.sprites.draw()

    def on_update(self, delta_time):
        if self.up or self.down:
            x_dir = math.cos(self.car.radians - math.pi / 2) * Consts.FORCE * (self.down - self.up)
            y_dir = math.sin(self.car.radians - math.pi / 2) * Consts.FORCE * (self.down - self.up)
            self.physics_engine.apply_force(self.car, (x_dir, y_dir))
            self.physics_engine.set_friction(self.car, 0)
        else:
            self.physics_engine.set_friction(self.car, 1.0)
        if self.right and not self.left:
            self.car.turning -= 1
        elif self.left and not self.right:
            self.car.turning += 1
        self.physics_engine.step()
        self.car.car_move(delta_time)
        self.camera.camera_move()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.up = True
        elif key == arcade.key.S:
            self.down = True
        elif key == arcade.key.A:
            self.left = True
        elif key == arcade.key.D:
            self.right = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.up = False
        elif key == arcade.key.S:
            self.down = False
        elif key == arcade.key.A:
            self.left = False
        elif key == arcade.key.D:
            self.right = False
