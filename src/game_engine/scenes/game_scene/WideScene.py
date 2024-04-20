from src.game_engine.scenes.game_scene.GameScene import GameScene
from src.render.sprites.BasicSprite import BasicSprite
from pyglet.math import Vec2 as Vector2D
from src.game_engine.scenes.game_scene.SceneSetup import WideSceneSetup


class WideScene(GameScene):
    def __init__(self):
        super().__init__()
        self.background = BasicSprite("assets/pic/map/Map.jpg", Vector2D(0, 0))
        self.background.update_scale(10)
        self.down_render_group.add(self.background)
        WideSceneSetup(self)
