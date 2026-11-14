import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pygame
import pytest

from lost_kingdom.core.game import Game
from lost_kingdom.core.settings import ASSET_DIR, SCREEN_SIZE, START
from lost_kingdom.core.states import Action, State
from lost_kingdom.entities.actor import Direction
from lost_kingdom.resources.assets import SPRITES, Resources
from lost_kingdom.resources.audio import Audio
from lost_kingdom.systems.level import COIN_SPAWNS, ENEMY_SPAWNS
from lost_kingdom.systems.world import Controls
from main import main


@pytest.fixture
def game():
    game = Game()
    yield game
    game.audio.pause(False)
    game.audio.stop_effects()


def key(game, value):
    game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=value))


def test_menu_pause_and_new_game_reset(game):
    assert game.state is State.MENU
    key(game, pygame.K_RETURN)
    assert game.state is State.PLAYING
    game.scene.world.player.coins = 7
    game.scene.world.player.health = 1
    game.scene.world.player.attack(game.settings)
    key(game, pygame.K_ESCAPE)
    before = game.scene.world.player.position.copy()
    cooldown = game.scene.world.player.cooldown
    game.advance(10, Controls(pygame.Vector2(1, 0), True))
    assert game.state is State.PAUSED
    assert game.scene.world.player.position == before
    assert game.scene.world.player.cooldown == cooldown
    key(game, pygame.K_ESCAPE)
    assert game.state is State.PLAYING
    game.activate(Action.MENU)
    key(game, pygame.K_RETURN)
    assert game.scene.world.player.health == 5
    assert game.scene.world.player.coins == 0
    assert game.scene.world.player.position == pygame.Vector2(START)
    assert game.scene.world.player.cooldown == 0
    assert len(game.scene.world.enemies) == len(ENEMY_SPAWNS)
    assert len(game.scene.world.coins) == len(COIN_SPAWNS)


@pytest.mark.parametrize("state", [State.GAME_OVER, State.VICTORY])
def test_end_screens_return_to_menu(game, state):
    game.transition(state)
    key(game, pygame.K_RETURN)
    assert game.state is State.MENU


def test_mouse_buttons_after_letterboxed_resize(game):
    game.handle_event(pygame.event.Event(pygame.VIDEORESIZE, w=1200, h=720))
    game.draw()
    assert game.mouse_position((0, 100)) is None
    rect = game.buttons()[0][2]
    position = (rect.centerx + game.viewport.x, rect.centery)
    game.handle_event(
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=position, button=1)
    )
    assert game.state is State.PLAYING
    game.handle_event(pygame.event.Event(pygame.WINDOWFOCUSLOST))
    assert game.state is State.PAUSED


def test_keyboard_exit_and_window_close(game):
    key(game, pygame.K_DOWN)
    key(game, pygame.K_RETURN)
    assert not game.running
    game.running = True
    game.handle_event(pygame.event.Event(pygame.QUIT))
    assert not game.running


def test_real_event_loop_starts_and_exits(game):
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    pygame.time.set_timer(pygame.QUIT, 80, loops=1)
    try:
        game.run()
    finally:
        pygame.time.set_timer(pygame.QUIT, 0)
    assert game.state is State.PLAYING
    assert not game.running
    assert game.scene.world.elapsed > 0


def test_actual_gameplay_triggers_victory_and_audio_once(game):
    game.activate(Action.START)
    game.scene.world.player.position.update(game.level.goal.center)
    game.scene.world.enemies.clear()
    with patch.object(game.audio, "play") as play:
        game.advance(0.01, Controls())
        game.advance(0.01, Controls())
    assert game.state is State.VICTORY
    play.assert_called_once_with("winning-level")


@pytest.mark.parametrize("state", list(State))
def test_screens_render_with_real_assets(game, state):
    game.transition(state)
    frame = game.draw()
    assert frame.get_size() == SCREEN_SIZE
    assert frame.get_at((160, 100)) != frame.get_at((0, 0))
    assert pygame.mixer.music.get_busy() or state is State.PAUSED


@pytest.mark.parametrize(
    ("kind", "directions"),
    [
        ("player", (Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP)),
        ("enemy", (Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT)),
    ],
)
def test_animation_frames_match_sprite_sheet_directions(kind, directions):
    resources = Resources()
    for animation, filename in SPRITES[kind].items():
        sheet = pygame.image.load(ASSET_DIR / kind / filename).convert_alpha()
        for row, facing in enumerate(directions):
            expected = pygame.transform.scale(
                sheet.subsurface((0, row * 64, 64, 64)), (128, 128)
            )
            actual = resources.frame(kind, animation, facing, 0)
            assert pygame.image.tobytes(actual, "RGBA") == pygame.image.tobytes(
                expected, "RGBA"
            ), (kind, animation, facing)


def test_no_audio_device_is_reported(caplog):
    with patch("pygame.mixer.init", side_effect=pygame.error("No audio device")):
        audio = Audio()
    assert not audio.available
    assert audio.warning
    assert "No audio device" in caplog.text
    audio.play("player-hit")
    audio.pause(True)


def test_entry_point_runs_and_closes_pygame():
    with patch("main.Game") as game, patch("pygame.quit") as quit_pygame:
        main()
    game.return_value.run.assert_called_once()
    quit_pygame.assert_called_once()


def test_missing_asset_is_reported_and_exits_unsuccessfully(caplog):
    with (
        patch("main.Game", side_effect=FileNotFoundError("Missing map.png")),
        patch("main.show_error") as show_error,
        patch("pygame.quit") as quit_pygame,
        pytest.raises(SystemExit, match="1"),
    ):
        main()
    assert "Missing map.png" in caplog.text
    show_error.assert_called_once_with("Missing map.png")
    quit_pygame.assert_called_once()


def test_game_loads_assets_outside_project_directory(tmp_path):
    code = """
import sys

sys.path.insert(0, sys.argv[1])

import pygame
from lost_kingdom.core.game import Game

try:
    game = Game()
    game.draw()
    assert game.audio.available
    assert pygame.mixer.music.get_busy()
finally:
    pygame.quit()
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(Path(__file__).resolve().parents[1] / "src")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
