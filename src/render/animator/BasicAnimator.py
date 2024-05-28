from typing import Any


def ease_in_out(t: float) -> float:
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0

    return t * t * (3.0 - 2.0 * t)


def lerp_ease_in_out(a: Any, b: Any, t: float) -> Any:
    if t <= 0.0:
        return a
    if t >= 1.0:
        return b

    return a + (b - a) * ease_in_out(t)


class BasicAnimator:
    def __init__(self, instance: Any, duration: float = -1) -> None:
        self._instance = instance
        self._duration = duration
        self._time = 0

    def update(self, dt: float) -> None:
        self._time += dt

        if self._time > self._duration != -1:
            self._time = self._duration

    def is_done(self) -> bool:
        return self._time >= self._duration != -1

    def reset(self) -> None:
        self._time = 0
