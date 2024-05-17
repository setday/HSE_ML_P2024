import gym
from gym import spaces
import numpy as np
from src.game_engine.scenes.game_scene.GameScene import GameScene
from gym_game.envs.Game import Game


class CustomEnv(gym.Env):
    def __init__(self):
        self.game = Game()
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Box(
            np.array(
                [-10000, -10000, -10000, -10000, -10000, -10000, -10000],
                dtype=np.float32,
            ),
            np.array(
                [10000, 10000, 10000, 10000, 10000, 10000, 10000], dtype=np.float32
            ),
        )

    def reset(
        self,
        *,
        seed=None,
        options=None,
    ):
        if not hasattr(self, "game"):
            self.game = Game()
        else:
            self.game.core.scene = GameScene(True)
        self.game.time = 0
        return self.game.observe(), {}

    def step(self, action):
        self.game.action(action)
        obs = self.game.observe()
        reward = self.game.evaluate()
        done = self.game.is_done()
        return obs, reward, done, False, {}

    def close(self):
        del self.game
