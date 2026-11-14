import pygame

from lost_kingdom.ui.components import GOLD, MUTED, UI


def draw_hud(
    target: pygame.Surface, ui: UI, health: int, maximum: int, coins: int
) -> None:
    ui.panel(target, pygame.Rect(20, 18, 212, 76))
    ui.text(target, "VIDA", (35, 29), 20, MUTED)
    for index in range(maximum):
        ui.heart(target, (35 + index * 36, 55), index < health)
    ui.panel(target, pygame.Rect(756, 18, 184, 76))
    ui.text(target, "MOEDAS", (777, 29), 20, MUTED)
    ui.coin(target, (785, 67), 16)
    ui.text(target, f"{coins:02d}", (808, 51), 34, GOLD)
    ui.panel(target, pygame.Rect(20, 650, 616, 50))
    ui.text(
        target,
        "WASD / SETAS  mover    SPACE  atacar    ESC  pausar",
        (36, 668),
        23,
    )
