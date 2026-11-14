import os
from collections.abc import Iterator

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import pytest

from lost_kingdom.core.settings import Settings
from lost_kingdom.systems.level import Level
from lost_kingdom.systems.world import World


@pytest.fixture(scope="session", autouse=True)
def pygame_session() -> Iterator[None]:
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_mode((960, 720))
    yield
    pygame.quit()


@pytest.fixture(scope="session")
def level() -> Level:
    return Level()


@pytest.fixture
def world(level: Level) -> World:
    world = World(level, Settings())
    world.enemies.clear()
    world.coins.clear()
    world.player.position.update(600, 1190)
    return world
