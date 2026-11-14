import pygame

from lost_kingdom.core.states import Action
from lost_kingdom.ui.components import RED, UI, Button, menu_buttons


def buttons() -> list[Button]:
    return menu_buttons([(Action.MENU, "MENU INICIAL"), (Action.EXIT, "EXIT")], 386)


def draw(target: pygame.Surface, ui: UI, selected: int, coins: int) -> None:
    ui.overlay_panel(target)
    ui.result(target, "GAME OVER", "O reino ainda precisa de voce.", RED, coins)
    ui.buttons(target, buttons(), selected)
