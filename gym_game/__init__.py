from gym.envs.registration import register

register(
    id="Parkme",
    entry_point="gym_game.envs:CustomEnv",
    max_episode_steps=2000,
)
