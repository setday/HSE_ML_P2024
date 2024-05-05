from typing import Any

from src.render.animator.BasicAnimator import BasicAnimator, lerp_ease_in_out


class MoverParameterAnimator(BasicAnimator):
    def __init__(self, parameter: Any, target: Any, duration: float):
        super().__init__(parameter, duration)
        self.target = target
        self.start = parameter

    def update(self, dt: float) -> Any:
        if self.is_done():
            return self._instance

        super().update(dt)

        self._instance = lerp_ease_in_out(self.start, self.target, self._time * self._duration)
        return self._instance


class MoverAnimator(BasicAnimator):
    def __init__(self, instance: Any, target: tuple[float, float], duration: float):
        if not hasattr(instance, 'x') or not hasattr(instance, 'y'):
            raise ValueError('Instance must have x and y attributes')

        super().__init__(instance, duration)

        self.xAnimator = MoverParameterAnimator(instance.x, target[0], duration)
        self.yAnimator = MoverParameterAnimator(instance.y, target[1], duration)

        self.target = target

    def update(self, dt: float) -> None:
        if self.is_done():
            return

        super().update(dt)

        new_x = self.xAnimator.update(dt)
        new_y = self.yAnimator.update(dt)

        self._instance.x = new_x
        self._instance.y = new_y
