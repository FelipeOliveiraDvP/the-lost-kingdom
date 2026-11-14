from dataclasses import dataclass
from enum import Enum
from typing import Self

import pygame

from lost_kingdom.core.settings import BODY_SIZE


class Direction(Enum):
    LEFT = (0, -1, 0)
    RIGHT = (1, 1, 0)
    DOWN = (2, 0, 1)
    UP = (3, 0, -1)

    @property
    def row(self) -> int:
        return self.value[0]

    @property
    def vector(self) -> pygame.Vector2:
        return pygame.Vector2(self.value[1:])

    @classmethod
    def from_vector(cls, vector: pygame.Vector2) -> Self:
        if abs(vector.x) > abs(vector.y):
            return cls.RIGHT if vector.x > 0 else cls.LEFT
        return cls.DOWN if vector.y > 0 else cls.UP


@dataclass
class Actor:
    position: pygame.Vector2
    facing: Direction = Direction.DOWN
    moving: bool = False
    animation_time: float = 0.0

    @property
    def body(self) -> pygame.Rect:
        rect = pygame.Rect((0, 0), BODY_SIZE)
        rect.center = (round(self.position.x), round(self.position.y))
        return rect
