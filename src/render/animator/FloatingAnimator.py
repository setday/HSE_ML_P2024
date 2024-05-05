from math import sin
from typing import Any

from src.render.animator.BasicAnimator import BasicAnimator


class FloatingParameterAnimator(BasicAnimator):
    def __init__(self, parameter: Any, limits: tuple[float, float], speed: float):
        super().__init__(parameter)
        self.limits = limits
        self.speed = speed

        self.amplitude = (limits[1] - limits[0]) / 2
        self.center = (limits[1] + limits[0]) / 2
        self.phase = 0

    def update(self, dt: float) -> Any:
        super().update(dt)

        return self.center + self.amplitude * sin(self.speed * self._time + self.phase)


class FloatingAnimator(BasicAnimator):
    def __init__(
        self,
        instance: Any,
        limits_x: tuple[float, float] = (0, 0),
        limits_y: tuple[float, float] = (-10, 10),
        speed: float = 1,
    ):
        if not hasattr(instance, "x") or not hasattr(instance, "y"):
            raise ValueError("Instance must have x and y attributes")

        super().__init__(instance)

        self.speed = speed

        self.xAnimator = FloatingParameterAnimator(limits_x[0], limits_x, speed)
        self.yAnimator = FloatingParameterAnimator(limits_y[0], limits_y, speed)

    def update(self, dt: float) -> None:
        super().update(dt)

        new_x = self.xAnimator.update(dt)
        new_y = self.yAnimator.update(dt)

        self._instance.x = new_x
        self._instance.y = new_y
