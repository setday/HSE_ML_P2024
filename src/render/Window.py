import arcade
from src.game_engine.entities.Camera import Camera
from src.game_engine.scenes.GameScene import GameScene
from src.game_engine.entities.Car import Car


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.scene = GameScene(self)
        self.car = Car(self.scene.space)
        self.camera = Camera(self.car)
        self.scene.add_sprite("PLayer", self.car)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(1024, 1024, 2048, 2048, self.scene.background)
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time):
        self.scene.space.step(1 / 60)
        self.car.apply_friction()
        self.car.sync()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.car.accelerate()
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.car.brake()
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.car.turn_left()
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.car.turn_right()
        if key == arcade.key.SPACE:
            self.car.hand_brake()
        if key == arcade.key.R:
            self.car.car_model.body.velocity = (0, 0)

    def on_key_release(self, key, modifiers):
        pass
