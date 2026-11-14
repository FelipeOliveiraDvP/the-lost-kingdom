import pygame

from lost_kingdom.core.states import Action
from lost_kingdom.ui.components import CREAM, GOLD, MUTED, UI, Button, menu_buttons


def buttons() -> list[Button]:
    return menu_buttons([(Action.START, "START GAME"), (Action.EXIT, "EXIT")], 350)


def draw(target: pygame.Surface, ui: UI, selected: int) -> None:
    ui.overlay_panel(target)
    ui.text(target, "UMA AVENTURA PIXEL ART", (480, 147), 22, MUTED, True)
    ui.text(target, "THE LOST", (480, 207), 68, CREAM, True)
    ui.text(target, "KINGDOM", (480, 266), 82, GOLD, True)
    ui.text(target, "Encontre o santuario ao norte.", (480, 315), 26, MUTED, True)
    ui.text(
        target,
        "W / A / S / D  ou  SETAS: movimentar",
        (480, 514),
        24,
        CREAM,
        True,
    )
    ui.text(
        target,
        "SPACE: atacar    |    ESC: pausar",
        (480, 546),
        24,
        CREAM,
        True,
    )
    ui.buttons(target, buttons(), selected)
