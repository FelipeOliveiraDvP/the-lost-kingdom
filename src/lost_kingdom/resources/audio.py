import logging
from pathlib import Path

import pygame

from lost_kingdom.core.settings import ASSET_DIR


class Audio:
    def __init__(self, root: Path = ASSET_DIR) -> None:
        self.available = False
        self.warning = ""
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            pygame.mixer.init(buffer=512)
        except pygame.error as error:
            logging.warning("Audio unavailable: %s", error)
            self.warning = "Audio indisponivel neste dispositivo."
            return
        for name in (
            "enemy-dying",
            "getting-coin",
            "player-dying",
            "player-hit",
            "winning-level",
        ):
            sound = pygame.mixer.Sound(root / "sound" / f"{name}.wav")
            sound.set_volume(0.5)
            self.sounds[name] = sound
        pygame.mixer.music.load(root / "sound" / "background-music.mp3")
        pygame.mixer.music.set_volume(0.22)
        pygame.mixer.music.play(-1)
        self.available = True

    def play(self, event: str) -> None:
        if self.available:
            self.sounds[event].play()

    def pause(self, paused: bool) -> None:
        if self.available:
            if paused:
                pygame.mixer.music.pause()
                pygame.mixer.pause()
            else:
                pygame.mixer.music.unpause()
                pygame.mixer.unpause()

    def stop_effects(self) -> None:
        if self.available:
            pygame.mixer.stop()
