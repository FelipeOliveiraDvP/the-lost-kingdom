import pygame

from lost_kingdom.core.states import Action
from lost_kingdom.ui.components import GOLD, UI, Button, menu_buttons


def buttons() -> list[Button]:
    return menu_buttons([(Action.MENU, "MENU INICIAL"), (Action.EXIT, "EXIT")], 386)


def draw(target: pygame.Surface, ui: UI, selected: int, coins: int) -> None:
    ui.overlay_panel(target)
    ui.result(target, "YOU WIN!", "Voce alcancou o santuario!", GOLD, coins)
    ui.buttons(target, buttons(), selected)
