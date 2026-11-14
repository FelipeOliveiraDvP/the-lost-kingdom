from enum import Enum, auto

import pygame

from lost_kingdom.entities import State
from lost_kingdom.settings import SCREEN_SIZE

INK = (15, 25, 35)
PANEL = (23, 38, 48)
GOLD = (241, 194, 96)
CREAM = (248, 237, 204)
MUTED = (164, 188, 184)
GREEN = (97, 205, 142)
RED = (225, 79, 87)

type Color = tuple[int, int, int]


class Action(Enum):
    START = auto()
    RESUME = auto()
    MENU = auto()
    EXIT = auto()


def buttons(state: State) -> list[tuple[Action, str, pygame.Rect]]:
    match state:
        case State.MENU:
            items = [(Action.START, "START GAME"), (Action.EXIT, "EXIT")]
            top = 350
        case State.PAUSED:
            items = [
                (Action.RESUME, "CONTINUAR"),
                (Action.MENU, "MENU INICIAL"),
                (Action.EXIT, "EXIT"),
            ]
            top = 330
        case State.GAME_OVER | State.VICTORY:
            items = [(Action.MENU, "MENU INICIAL"), (Action.EXIT, "EXIT")]
            top = 386
        case _:
            return []
    return [
        (action, label, pygame.Rect(320, top + index * 66, 320, 52))
        for index, (action, label) in enumerate(items)
    ]


class UI:
    def __init__(self) -> None:
        self.fonts: dict[int, pygame.font.Font] = {}

    def text(
        self,
        target: pygame.Surface,
        value: str,
        position: tuple[int, int],
        size: int = 26,
        color: Color = CREAM,
        centered: bool = False,
    ) -> None:
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(None, size)
        image = self.fonts[size].render(value, True, color)
        rect = image.get_rect()
        if centered:
            rect.center = position
        else:
            rect.topleft = position
        target.blit(image, rect)

    @staticmethod
    def panel(target: pygame.Surface, rect: pygame.Rect) -> None:
        pygame.draw.rect(target, INK, rect.move(4, 5))
        pygame.draw.rect(target, PANEL, rect)
        pygame.draw.rect(target, GOLD, rect, 2)
        pygame.draw.rect(target, (61, 74, 69), rect.inflate(-10, -10), 1)

    @staticmethod
    def heart(target: pygame.Surface, position: tuple[int, int], filled: bool) -> None:
        x, y = position
        points = (
            (0, 2),
            (2, 0),
            (4, 0),
            (6, 2),
            (8, 0),
            (10, 0),
            (12, 2),
            (12, 5),
            (6, 11),
            (0, 5),
        )
        polygon = [(x + px * 2, y + py * 2) for px, py in points]
        pygame.draw.polygon(target, RED if filled else (57, 73, 78), polygon)
        if filled:
            pygame.draw.rect(target, (255, 162, 151), (x + 4, y + 4, 4, 4))

    @staticmethod
    def coin(
        target: pygame.Surface, position: tuple[int, int], width: int = 12
    ) -> None:
        x, y = position
        rect = pygame.Rect(x - width // 2, y - 9, width, 18)
        pygame.draw.ellipse(target, (103, 66, 33), rect.move(0, 2))
        pygame.draw.ellipse(target, GOLD, rect)
        if width > 5:
            pygame.draw.ellipse(target, (255, 230, 146), rect.inflate(-4, -4), 2)

    def hud(
        self, target: pygame.Surface, health: int, maximum: int, coins: int
    ) -> None:
        self.panel(target, pygame.Rect(20, 18, 212, 76))
        self.text(target, "VIDA", (35, 29), 20, MUTED)
        for index in range(maximum):
            self.heart(target, (35 + index * 36, 55), index < health)
        self.panel(target, pygame.Rect(756, 18, 184, 76))
        self.text(target, "MOEDAS", (777, 29), 20, MUTED)
        self.coin(target, (785, 67), 16)
        self.text(target, f"{coins:02d}", (808, 51), 34, GOLD)
        self.panel(target, pygame.Rect(20, 650, 616, 50))
        self.text(
            target,
            "WASD / SETAS  mover    SPACE  atacar    ESC  pausar",
            (36, 668),
            23,
        )

    def overlay(
        self,
        target: pygame.Surface,
        state: State,
        selected: int,
        coins: int = 0,
    ) -> None:
        shade = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        shade.fill((5, 15, 24, 185))
        target.blit(shade, (0, 0))
        self.panel(target, pygame.Rect(160, 100, 640, 520))
        if state is State.MENU:
            self.text(target, "UMA AVENTURA PIXEL ART", (480, 147), 22, MUTED, True)
            self.text(target, "THE LOST", (480, 207), 68, CREAM, True)
            self.text(target, "KINGDOM", (480, 266), 82, GOLD, True)
            self.text(
                target, "Encontre o santuario ao norte.", (480, 315), 26, MUTED, True
            )
            self.text(
                target,
                "W / A / S / D  ou  SETAS: movimentar",
                (480, 514),
                24,
                CREAM,
                True,
            )
            self.text(
                target,
                "SPACE: atacar    |    ESC: pausar",
                (480, 546),
                24,
                CREAM,
                True,
            )
        elif state is State.PAUSED:
            self.text(target, "PAUSADO", (480, 210), 64, GOLD, True)
            self.text(
                target, "A aventura espera por voce.", (480, 272), 28, MUTED, True
            )
        else:
            won = state is State.VICTORY
            self.text(
                target,
                "YOU WIN!" if won else "GAME OVER",
                (480, 215),
                72,
                GOLD if won else RED,
                True,
            )
            self.text(
                target,
                "Voce alcancou o santuario!"
                if won
                else "O reino ainda precisa de voce.",
                (480, 280),
                28,
                CREAM,
                True,
            )
            self.text(target, f"Moedas coletadas: {coins}", (480, 325), 32, GOLD, True)
        for index, (_, label, rect) in enumerate(buttons(state)):
            active = index == selected
            pygame.draw.rect(target, GOLD if active else INK, rect)
            pygame.draw.rect(target, GOLD if active else MUTED, rect, 2)
            self.text(
                target,
                (">  " if active else "") + label,
                rect.center,
                30,
                INK if active else CREAM,
                True,
            )
        self.text(
            target,
            "SETAS + ENTER  ou  clique para selecionar",
            (480, 585),
            21,
            MUTED,
            True,
        )
