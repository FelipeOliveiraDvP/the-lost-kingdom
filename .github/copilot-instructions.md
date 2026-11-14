# Copilot instructions

## Project status and architecture

This repository is named The Lost Kingdom, but its current Python application is
still a starter scaffold: `src/main.py` only prints a setup message. The intended
game is a top-down 2D action RPG. Its mechanics, game states, and suggested
modular responsibilities are described in `docs/game-design.md`; treat that
document as the design target, not as evidence that those systems already exist.

The planned game uses Pygame, with separate responsibilities for the main game
loop, game states/scenes, entities, collision and combat, levels, and HUD. The
current assets are organized under `assets/` by player, enemy, and sound, with
the map image at the asset root. Use the existing files and exact filenames
when wiring assets into the game.

`src/main.py` is the current executable entry point. Tests are under `tests/`.
Project dependencies, Poe tasks, pytest discovery, Ruff, and strict mypy
configuration are defined in `pyproject.toml`.

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
uv run pytest tests/test_main.py::test_basic_operation
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
- The game design calls for a Python/Pygame application, but Pygame is not
  currently listed as a project dependency. Update project dependencies when
  introducing runtime use of it.
