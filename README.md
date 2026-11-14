# hello-python

A minimal Python project that prints a message when run.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) for installing the project’s development tools

## Setup

From the project directory, install the development dependencies:

```bash
uv sync --group dev
```

## Run

```bash
uv run python src/main.py
```

The program prints:

```text
Python environment configured successfully!
```

## Development checks

Run linting, type checking, and the test suite:

```bash
uv run poe check
```

Individual commands:

```bash
uv run poe lint
uv run poe typecheck
uv run poe test
uv run pytest tests/test_main.py::test_basic_operation
uv run poe format
```
