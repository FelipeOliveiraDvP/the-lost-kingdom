from enum import Enum, auto


class State(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class Action(Enum):
    START = auto()
    RESUME = auto()
    MENU = auto()
    EXIT = auto()
