import pygame

from lost_kingdom.core.states import Action
from lost_kingdom.ui.components import GOLD, MUTED, UI, Button, menu_buttons


def buttons() -> list[Button]:
    return menu_buttons(
        [
            (Action.RESUME, "CONTINUAR"),
            (Action.MENU, "MENU INICIAL"),
            (Action.EXIT, "EXIT"),
        ],
        330,
    )


def draw(target: pygame.Surface, ui: UI, selected: int) -> None:
    ui.overlay_panel(target)
    ui.text(target, "PAUSADO", (480, 210), 64, GOLD, True)
    ui.text(target, "A aventura espera por voce.", (480, 272), 28, MUTED, True)
    ui.buttons(target, buttons(), selected)
