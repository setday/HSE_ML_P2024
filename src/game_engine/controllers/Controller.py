import arcade
import numpy
import random


class Controller:
    def __init__(self):
        self.car = None

    def handle_input(self, keys=None, observation=None):
        pass

    def connect_car(self, car):
        self.car = car


class KeyboardController(Controller):
    def __init__(self):
        super().__init__()

    def handle_input(self, keys=None, observation=None):
        if keys.get(arcade.key.LEFT, False) or keys.get(arcade.key.A, False):
            self.car.turn_left(keys.get(arcade.key.SPACE, False))
        if keys.get(arcade.key.RIGHT, False) or keys.get(arcade.key.D, False):
            self.car.turn_right(keys.get(arcade.key.SPACE, False))
        if keys.get(arcade.key.UP, False) or keys.get(arcade.key.W, False):
            self.car.forward_accelerate()
        if keys.get(arcade.key.DOWN, False) or keys.get(arcade.key.S, False):
            self.car.backward_acceleration()
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
            5,  # hand_break
        ]
        self.probabilities = list(
            map(lambda x: x / sum(self.probabilities), self.probabilities)
        )
        self.probabilities = [
            sum(self.probabilities[:i]) for i in range(len(self.probabilities) + 1)
        ]

    def handle_input(self, keys=None, observation=None):
        if self.timer == 0:
            self.action_kind = random.random()
            self.timer = 30
        if self.probabilities[0] <= self.action_kind < self.probabilities[1]:
            self.car.forward_accelerate()
        elif self.probabilities[1] <= self.action_kind < self.probabilities[2]:
            self.car.turn_left(False)
        elif self.probabilities[2] <= self.action_kind < self.probabilities[3]:
            self.car.turn_right(False)
        elif self.probabilities[3] <= self.action_kind < self.probabilities[4]:
            self.car.backward_acceleration()
        else:
            self.car.hand_brake()
        self.timer -= 1


class BrakeController(Controller):
    def __init__(self):
        super().__init__()

    def handle_input(self, keys=None, observation=None):
        self.car.hand_brake()


class AIController(Controller):
    def __init__(self, weights_file=None):
        super().__init__()

    def link_model(self, model):
        # for the begining input: car pos & ang and park_plc pos & ang
        self.model = model

    def handle_input(self, keys=None, observation=None):
        # order: accelerate, turn_left, turn_right, brake, hand_brake
        # probs = self.model.predict(numpy.array(observation))

        probs = self.model.activate(observation)
        # print(probs)

        # TODO: choose "right weight" instead of 0.5
        action_kinds = [(probs[i] >= 0.5) for i in range(5)]
        if action_kinds[0]:
            self.car.forward_accelerate()
        if action_kinds[1]:
            self.car.turn_left(action_kinds[4])
        if action_kinds[2]:
            self.car.turn_right(action_kinds[4])
        if action_kinds[3]:
            self.car.backward_acceleration()
