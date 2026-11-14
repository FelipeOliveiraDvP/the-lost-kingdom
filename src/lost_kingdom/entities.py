from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Self

import pygame

from lost_kingdom.settings import BODY_SIZE, START, Settings


class State(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


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


class Player(Actor):
    def __init__(self, settings: Settings) -> None:
        super().__init__(pygame.Vector2(START), Direction.UP)
        self.health = settings.max_health
        self.coins = 0
        self.cooldown = 0.0
        self.attack_left = 0.0
        self.invulnerable_left = 0.0
        self.hurt_left = 0.0

    def tick(self, dt: float) -> None:
        self.animation_time += dt
        self.cooldown = max(0.0, self.cooldown - dt)
        self.attack_left = max(0.0, self.attack_left - dt)
        self.invulnerable_left = max(0.0, self.invulnerable_left - dt)
        self.hurt_left = max(0.0, self.hurt_left - dt)

    def attack(self, settings: Settings) -> bool:
        if self.cooldown > 1e-9 or self.health == 0:
            return False
        self.cooldown = settings.attack_cooldown
        self.attack_left = settings.attack_duration
        return True

    @property
    def attack_box(self) -> pygame.Rect:
        x, y = round(self.position.x), round(self.position.y)
        match self.facing:
            case Direction.LEFT:
                return pygame.Rect(x - 60, y - 23, 60, 46)
            case Direction.RIGHT:
                return pygame.Rect(x, y - 23, 60, 46)
            case Direction.UP:
                return pygame.Rect(x - 23, y - 60, 46, 60)
            case Direction.DOWN:
                return pygame.Rect(x - 23, y, 46, 60)

    def take_damage(self, settings: Settings) -> bool:
        if self.invulnerable_left > 1e-9 or self.health == 0:
            return False
        self.health -= 1
        self.invulnerable_left = settings.invulnerability
        self.hurt_left = 0.22
        return True


@dataclass
class Enemy(Actor):
    health: int = 1
    patrol_direction: int = 1
    contact_left: float = 0.0
    home: pygame.Vector2 = field(init=False)

    def __post_init__(self) -> None:
        self.home = self.position.copy()


@dataclass
class Coin:
    position: pygame.Vector2

    @property
    def body(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.position.x) - 10, round(self.position.y) - 10, 20, 20
        )


@dataclass
class FallenEnemy:
    position: pygame.Vector2
    facing: Direction
    age: float = 0.0
