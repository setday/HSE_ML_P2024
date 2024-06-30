from typing import Any

from typing_extensions import Protocol

from pyglet.math import Vec2 as Vector2D  # type: ignore[import-untyped]


class ObjBunch:
    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)


class PositionalClass(Protocol):
    position: Vector2D | tuple[float, float]
