import pickle
import random

import arcade
import numpy as np
import torch
from stable_baselines3 import DQN, A2C, PPO

from models.DQNPolicy import DQNPolicy
from src.game_engine.entities.Car import Car


class Controller:
    def __init__(self) -> None:
        self.car: Car | None = None

    def handle_input(self, keys=None, observation=None) -> None:
        pass

    def connect_car(self, car: Car) -> None:
        self.car = car


class KeyboardController(Controller):
    def __init__(self) -> None:
        super().__init__()

    def handle_input(self, keys: dict = None, observation: list[float] | np.ndarray = None) -> None:
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
    def __init__(self) -> None:
        super().__init__()
        self.timer: float = 0
        self.action_kind: int = 0
        self.probabilities: list[int] = [
            10,  # accelerate
            5,  # turn left
            15,  # turn right
            0,  # brake
            5,  # hand_break
        ]
        self.probabilities: list[float] = list(
            map(lambda x: x / sum(self.probabilities), self.probabilities)
        )
        self.probabilities: list[float] = [
            sum(self.probabilities[:i]) for i in range(len(self.probabilities) + 1)
        ]

    def handle_input(self, keys: dict = None, observation: list[float] | np.ndarray = None) -> None:
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
    def __init__(self) -> None:
        super().__init__()

    def handle_input(self, keys: dict = None, observation: list[float] | np.ndarray = None) -> None:
        self.car.hand_brake()


class AIController(Controller):

    def __init__(self, configs: dict) -> None:
        super().__init__()
        self.type = configs.get("type")
        path = configs.get("path")
        if self.type == "neat":
            # TODO: load neat model
            pass
        elif self.type == "sklearn":
            with open(path, "rb") as model:
                self.model = pickle.load(model)
        elif self.type == "pytorch":
            self.model = DQNPolicy(9, 4)
            self.model.dqn.load_state_dict(torch.load(path))
        elif self.type == "stable_baselines":
            if configs.get("policy") == "A2C":
                self.model = A2C.load(path)
            elif configs.get("policy") == "DQN":
                self.model = DQN.load(path)
            elif configs.get("policy") == "PPO":
                self.model = PPO.load(path)

    def link_model(self, model) -> None:
        # for the begining input: car pos & ang and park_plc pos & ang
        self.model = model

    def handle_input(self, keys: dict = None, observation: list[float] | np.ndarray = None) -> None:
        action: int = -1

        if self.type == "neat":
            # order: accelerate, turn_left, turn_right, brake, hand_brake
            probs = self.model.activate(observation)

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
            if action_kinds[4]:
                self.car.hand_brake()
            return
        elif self.type == "sklearn":
            probs = self.model.predict_proba([observation])[0]
            action = np.random.choice(list(range(9)), p=probs)
        elif self.type == "pytorch":
            with torch.no_grad():
                action = self.model.make_action(observation)
        elif self.type == "stable_baselines":
            action, _ = self.model.predict(observation)
        if action == 0:
            self.car.turn_left()
        if action == 1:
            self.car.turn_right()
        if action == 2:
            self.car.forward_accelerate()
        if action == 3:
            self.car.backward_acceleration()
        if action == 4:
            self.car.car_model.body.velocity = (0, 0)
        if action == 5:
            self.car.forward_accelerate()
            self.car.turn_left()
        if action == 6:
            self.car.forward_accelerate()
            self.car.turn_right()
        if action == 7:
            self.car.backward_acceleration()
            self.car.turn_left()
        if action == 8:
            self.car.backward_acceleration()
            self.car.turn_right()
