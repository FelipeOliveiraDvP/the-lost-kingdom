# Copilot instructions

## Project structure

- `src/main.py` is the current application entry point. Its `main()` function is run when the file is executed directly.
- Tests live in `tests/`; pytest is configured to discover `test_*.py` files and `test_*` functions there.
- Project metadata, development dependencies, and tool configuration are in `pyproject.toml`.

## Build, test, and lint

The project has no separate build task. Development commands are defined as Poe tasks in `pyproject.toml`:

- `poe check` runs lint, type checking, and tests.
- `poe test` runs the full pytest suite.
- `pytest tests/test_main.py::test_basic_operation` runs one test; replace the node ID to select another test.
- `poe lint` runs Ruff checks.
- `poe format` formats the project with Ruff.
- `poe typecheck` runs strict mypy checks on `src/`.

The development dependency group in `pyproject.toml` provides Poe, Ruff, pytest, and mypy. VS Code tasks invoke Poe from the workspace `.venv`.

## Code conventions

- Target Python 3.12 or newer and keep strict mypy compatibility for code under `src/`.
- Ruff formatting uses an 88-character line length. Its lint rules include pycodestyle errors, Pyflakes, import sorting, pyupgrade, and bugbear (`E`, `F`, `I`, `UP`, `B`).
- Preserve the existing pytest discovery names: test files use `test_*.py`, and test functions use the `test_*` prefix.
