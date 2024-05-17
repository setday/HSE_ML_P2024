import random
import pickle
import arcade
import numpy as np
import torch
from stable_baselines3 import DQN, A2C, PPO
from models.DQNPolicy import DQNPolicy


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

    def handle_input(self, keys):
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

    def handle_input(self, keys):
        self.car.hand_brake()


class AIController(Controller):
    def __init__(self, agent_type="sklearn"):
        super().__init__()
        self.agent_type = agent_type
        if agent_type == "pytorch":
            self.agent = DQNPolicy(9, 7)  # TODO: make parameters of the ctor
            self.agent.dqn.load_state_dict(torch.load("models_bin/torch.pt"))
        elif agent_type == "sklearn":
            with open("models_bin/CEM5.pkl", "rb") as model:
                self.agent = pickle.load(model)
        else:
            self.agent = PPO.load("models_bin/PPO")

    def handle_input(self, keys):
        if self.agent_type == "pytorch":
            with torch.no_grad():
                action = self.agent.make_action(keys)
        elif self.agent_type == "sklearn":
            probs = self.agent.predict_proba([keys])[0]
            action = np.random.choice(list(range(9)), p=probs)
        else:
            action, _ = self.agent.predict(keys)
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

        # if keys.get(arcade.key.SPACE, False):
        #     self.car.hand_brake()
