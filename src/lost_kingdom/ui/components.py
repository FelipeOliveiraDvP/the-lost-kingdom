import pygame

from lost_kingdom.core.settings import SCREEN_SIZE
from lost_kingdom.core.states import Action

INK = (15, 25, 35)
PANEL = (23, 38, 48)
GOLD = (241, 194, 96)
CREAM = (248, 237, 204)
MUTED = (164, 188, 184)
GREEN = (97, 205, 142)
RED = (225, 79, 87)

type Color = tuple[int, int, int]
type Button = tuple[Action, str, pygame.Rect]


def menu_buttons(items: list[tuple[Action, str]], top: int) -> list[Button]:
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

    def overlay_panel(self, target: pygame.Surface) -> None:
        shade = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        shade.fill((5, 15, 24, 185))
        target.blit(shade, (0, 0))
        self.panel(target, pygame.Rect(160, 100, 640, 520))

    def result(
        self,
        target: pygame.Surface,
        title: str,
        message: str,
        color: Color,
        coins: int,
    ) -> None:
        self.text(target, title, (480, 215), 72, color, True)
        self.text(target, message, (480, 280), 28, CREAM, True)
        self.text(target, f"Moedas coletadas: {coins}", (480, 325), 32, GOLD, True)

    def buttons(
        self, target: pygame.Surface, choices: list[Button], selected: int
    ) -> None:
        for index, (_, label, rect) in enumerate(choices):
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
