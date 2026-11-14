import logging

import pygame

from lost_kingdom.core.game import Game
from lost_kingdom.ui.error import show_error


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        Game().run()
    except (OSError, ValueError, pygame.error) as error:
        logging.exception("The Lost Kingdom could not run")
        show_error(str(error))
        raise SystemExit(1) from error
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
