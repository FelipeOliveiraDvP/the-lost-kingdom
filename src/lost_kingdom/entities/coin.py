from dataclasses import dataclass

import pygame


@dataclass
class Coin:
    position: pygame.Vector2

    @property
    def body(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.position.x) - 10, round(self.position.y) - 10, 20, 20
        )
