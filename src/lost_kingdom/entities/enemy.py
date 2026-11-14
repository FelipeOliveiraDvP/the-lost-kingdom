from dataclasses import dataclass, field

import pygame

from lost_kingdom.entities.actor import Actor, Direction


@dataclass
class Enemy(Actor):
    health: int = 1
    patrol_direction: int = 1
    contact_left: float = 0.0
    home: pygame.Vector2 = field(init=False)

    def __post_init__(self) -> None:
        self.home = self.position.copy()


@dataclass
class FallenEnemy:
    position: pygame.Vector2
    facing: Direction
    age: float = 0.0
