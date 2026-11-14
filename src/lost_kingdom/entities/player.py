import pygame

from lost_kingdom.core.settings import START, Settings
from lost_kingdom.entities.actor import Actor, Direction


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
