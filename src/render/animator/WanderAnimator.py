import random
from typing import Any

from .BasicAnimator import BasicAnimator, lerp_ease_in_out


class WanderParameterAnimator(BasicAnimator):
    def __init__(self, parameter: Any, limits: tuple[float, float], speed: float):
        super().__init__(parameter)
        self.limits = limits
        self.speed = speed

        self.targetValue = parameter
        self.startValue = parameter

    def update(self, dt: float) -> Any:
        super().update(dt)

        if abs(self.targetValue - self._instance) == 0:
            self.targetValue = random.uniform(*self.limits)
            self.startValue = self._instance
            self._time = 0

        self._instance = lerp_ease_in_out(
            self.startValue, self.targetValue, self._time * self.speed
        )

        return self._instance


class WanderAnimator(BasicAnimator):
    def __init__(
        self,
        instance: Any,
        limits_x: tuple[float, float],
        limits_y: tuple[float, float],
        speed: float = 1,
    ):
        if not hasattr(instance, "x") or not hasattr(instance, "y"):
            raise ValueError("Instance must have x and y attributes")

        super().__init__(instance)

        self.speed = speed

        self.xAnimator = WanderParameterAnimator(limits_x[0], limits_x, speed * 0.97)
        self.yAnimator = WanderParameterAnimator(limits_y[0], limits_y, speed * 1.03)

    def update(self, dt: float) -> None:
        super().update(dt)

        new_x = self.xAnimator.update(dt)
        new_y = self.yAnimator.update(dt)

        self._instance.x = new_x
        self._instance.y = new_y
