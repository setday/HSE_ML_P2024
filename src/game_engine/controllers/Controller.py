import arcade
import random


class Controller:
    def __init__(self):
        self.car = None

    def handle_input(self, keys):
        pass

    def connect_car(self, car):
        self.car = car


class KeyboardController(Controller):
    def __init__(self):
        super().__init__()

    def handle_input(self, keys):
        if keys.get(arcade.key.LEFT, False) or keys.get(arcade.key.A, False):
            self.car.turn_left(keys.get(arcade.key.SPACE, False))
        if keys.get(arcade.key.RIGHT, False) or keys.get(arcade.key.D, False):
            self.car.turn_right(keys.get(arcade.key.SPACE, False))
        if keys.get(arcade.key.UP, False) or keys.get(arcade.key.W, False):
            self.car.accelerate()
        if keys.get(arcade.key.DOWN, False) or keys.get(arcade.key.S, False):
            self.car.brake()
        if keys.get(arcade.key.R, False):
            self.car.car_model.body.velocity = (0, 0)

        if keys.get(arcade.key.SPACE, False):
            self.car.hand_brake()


class RandomController(Controller):
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.action_kind = 0
        self.probabilities = [
            10,  # accelerate
            5,  # turn left
            15,  # turn right
            0,  # brake
            0  # hand_break
        ]
        self.probabilities = list(map(lambda x: x / sum(self.probabilities), self.probabilities))
        self.probabilities = [sum(self.probabilities[:i]) for i in range(len(self.probabilities) + 1)]

    def handle_input(self, keys):
        if self.timer == 0:
            self.action_kind = random.random()
            self.timer = 30
        if self.probabilities[0] <= self.action_kind < self.probabilities[1]:
            self.car.accelerate()
        elif self.probabilities[1] <= self.action_kind < self.probabilities[2]:
            self.car.turn_left(False)
        elif self.probabilities[2] <= self.action_kind < self.probabilities[3]:
            self.car.turn_right(False)
        elif self.probabilities[3] <= self.action_kind < self.probabilities[4]:
            self.car.brake()
        else:
            self.car.hand_brake()
        self.timer -= 1
