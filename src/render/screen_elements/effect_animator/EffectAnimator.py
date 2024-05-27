from src.render.screen_elements.effect_animator.BasicEffect import BasicEffect


class EffectAnimator:
    def __init__(self):
        self.animation_queue = []

    def add_effect(self, effect: BasicEffect):
        self.animation_queue.append(effect)

    def update(self, delta_time: float):
        if len(self.animation_queue) == 0:
            return

        effect = self.animation_queue[0]
        if effect.is_finished():
            self.animation_queue.pop(0)
            if effect.finish_callback is not None:
                effect.finish_callback()
        else:
            effect.update(delta_time)

    def draw(self):
        if len(self.animation_queue) == 0:
            return

        effect = self.animation_queue[0]
        effect.draw()
