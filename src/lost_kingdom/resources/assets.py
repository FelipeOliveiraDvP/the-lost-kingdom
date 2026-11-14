from pathlib import Path

import pygame

from lost_kingdom.core.settings import ASSET_DIR, MAP_SIZE
from lost_kingdom.entities.actor import Direction

type Frames = tuple[tuple[pygame.Surface, ...], ...]

SPRITE_ROWS = {
    "player": (1, 2, 0, 3),
    "enemy": (2, 3, 0, 1),
}

SPRITES = {
    "player": {
        "idle": "Swordsman_lvl1_Idle_with_shadow.png",
        "walk": "Swordsman_lvl1_Run_with_shadow.png",
        "attack": "Swordsman_lvl1_attack_with_shadow.png",
        "hurt": "Swordsman_lvl1_Hurt_with_shadow.png",
        "death": "Swordsman_lvl1_Death_with_shadow.png",
    },
    "enemy": {
        "idle": "orc1_idle_with_shadow.png",
        "walk": "orc1_walk_with_shadow.png",
        "attack": "orc1_attack_with_shadow.png",
        "death": "orc1_death_with_shadow.png",
    },
}


class Resources:
    def __init__(self, root: Path = ASSET_DIR) -> None:
        self.map = pygame.image.load(root / "map.png").convert()
        if self.map.get_size() != MAP_SIZE:
            raise ValueError(f"Map must be {MAP_SIZE} to match the collision layer.")
        self.sprites: dict[tuple[str, str], Frames] = {}
        for kind, animations in SPRITES.items():
            for animation, filename in animations.items():
                sheet = pygame.image.load(root / kind / filename).convert_alpha()
                width, height = sheet.get_size()
                if height != 256 or width % 64:
                    raise ValueError(f"Invalid 64x64 sprite sheet: {filename}")
                self.sprites[kind, animation] = tuple(
                    tuple(
                        pygame.transform.scale(
                            sheet.subsurface((column * 64, row * 64, 64, 64)),
                            (128, 128),
                        )
                        for column in range(width // 64)
                    )
                    for row in range(4)
                )
        self.minimap = pygame.transform.scale(self.map, (120, 160))

    def frame(
        self,
        kind: str,
        animation: str,
        facing: Direction,
        time: float,
        duration: float | None = None,
    ) -> pygame.Surface:
        row = SPRITE_ROWS[kind][facing.row]
        frames = self.sprites[kind, animation][row]
        index = (
            min(len(frames) - 1, int(max(0.0, time) / duration * len(frames)))
            if duration is not None
            else int(time * 10) % len(frames)
        )
        return frames[index]
