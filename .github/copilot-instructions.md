# Copilot instructions

## Project status and architecture

The Lost Kingdom is an implemented top-down 2D action RPG using Pygame. Its
mechanics, game states and adopted architecture are documented in
`docs/game-design.md`.

`src/main.py` is the executable entry point. Modules are organized under
`src/lost_kingdom/`:

- `core/settings.py` and `core/states.py`: configuration, states and menu actions.
- `core/game.py`: external composition, window, events, navigation and game loop.
- `entities/`: actors, directions, player, enemies and coins.
- `systems/`: level data, collision, combat and world simulation.
- `scenes/`: the gameplay world/camera/rendering and individual menu screens.
- `ui/`: shared drawing components, HUD and graphical error reporting.
- `resources/`: image/spritesheet loading and audio.

Entities must not import systems or presentation. Systems must not import
scenes, UI, resource loaders or `core/game.py`. Configuration and state modules
must not import the game loop. Keep package initializers free of device
initialization and game-loop imports. This is pragmatic modular architecture:
Pygame geometry and collision masks remain in the simulation.

Use the full new module paths; do not add compatibility facades for the former
flat modules. `Level.collision` owns collision operations, and `Game.scene.world`
is the current gameplay simulation.

Assets remain under `assets/` by player, enemy and sound, with `map.png` at the
asset root. Preserve their exact filenames. `ASSET_DIR` in `core/settings.py`
is anchored to the source location, not the working directory.

Tests are under `tests/`. Project dependencies, Poe tasks, pytest discovery,
Ruff and strict mypy configuration are defined in `pyproject.toml`.

## Build, test, and lint

Requires Python 3.12 or newer and uv. Install development tools with:

```bash
uv sync --group dev
```

Run the current application:

```bash
uv run python src/main.py
```

Run the full check (Ruff lint, strict mypy on `src/`, and pytest):

```bash
uv run poe check
```

Other useful commands:

```bash
uv run poe test
uv run pytest tests/test_main.py::test_entry_point_runs_and_closes_pygame
uv run poe lint
uv run poe typecheck
uv run poe format
```

Pytest discovers `test_*.py` files and `test_*` functions in `tests/`. There is
no separate build task.

## Code conventions

- Target Python 3.12+ and keep code under `src/` compatible with strict mypy.
- Ruff formatting uses an 88-character line length; lint rules are `E`, `F`,
  `I`, `UP`, and `B`.
- Preserve pytest's configured file and function naming patterns.
- Pygame is already a runtime dependency. Tests use SDL dummy video/audio drivers
  and verify both gameplay and rendering with the existing assets.
