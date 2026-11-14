from dataclasses import dataclass
from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parents[3] / "assets"
SCREEN_SIZE = (960, 720)
MAP_SIZE = (1086, 1448)
FPS = 60
BODY_SIZE = (22, 14)
START = (625, 1320)
GOAL = (508, 65, 72, 52)


@dataclass(frozen=True)
class Settings:
    player_speed: float = 180.0
    enemy_speed: float = 78.0
    chase_radius: float = 200.0
    attack_duration: float = 0.32
    attack_cooldown: float = 0.48
    invulnerability: float = 1.2
    max_health: int = 5

    def __post_init__(self) -> None:
        if (
            min(
                self.player_speed,
                self.enemy_speed,
                self.chase_radius,
                self.attack_duration,
                self.attack_cooldown,
                self.invulnerability,
            )
            <= 0
        ):
            raise ValueError("Movement and combat settings must be positive.")
        if self.attack_cooldown < self.attack_duration or self.max_health < 1:
            raise ValueError("Invalid attack cooldown or maximum health.")
