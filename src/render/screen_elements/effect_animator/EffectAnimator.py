import arcade

from src.render.screen_elements.effect_animator.BasicEffect import BasicEffect


class EffectAnimator:
    def __init__(self):
        self._camera = arcade.Camera()

        self._animation_queue = []
        self._post_animation_queue = []

    def add_effect(self, effect: BasicEffect):
        self._animation_queue.append(effect)

    def _add_post_effect(self, effect: BasicEffect):
        self._post_animation_queue.append(effect)

    def clear_effects(self):
        self._animation_queue = []

    def clear_post_effects(self):
        self._post_animation_queue = []

    def update(self, delta_time: float):
        for post_effect in self._post_animation_queue:
            post_effect.update(delta_time)

        if len(self._animation_queue) == 0:
            return

        effect = self._animation_queue[0]
        if effect.is_finished():
            self._animation_queue.pop(0)

            if effect.finish_callback is not None:
                effect.finish_callback()

            post_effect = effect.get_post_effect()
            if post_effect is not None:
                self._add_post_effect(post_effect)
        else:
            effect.update(delta_time)

    def draw(self):
        self._camera.use()

        for post_effect in self._post_animation_queue:
            post_effect.post_draw()

        if len(self._animation_queue) == 0:
            return

        effect = self._animation_queue[0]
        effect.draw()
