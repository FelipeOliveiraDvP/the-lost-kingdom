import textwrap

import pygame

from lost_kingdom.ui.components import GOLD, INK, UI


def show_error(message: str) -> None:
    window = pygame.display.get_surface()
    if window is None:
        return
    ui = UI()
    window.fill(INK)
    ui.text(window, "Nao foi possivel abrir o jogo.", (30, 35), 36, GOLD)
    for index, line in enumerate(textwrap.wrap(message, width=72)[:12]):
        ui.text(window, line, (30, 100 + index * 28), 24)
    ui.text(window, "ENTER / ESC para fechar.", (30, window.get_height() - 50), 24)
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_ESCAPE, pygame.K_RETURN)
        ):
            return
