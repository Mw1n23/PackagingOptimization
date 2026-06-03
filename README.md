# 3D Bin Packing Visualization

[![CI](https://github.com/Mw1n23/PackagingOptimization/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Mw1n23/PackagingOptimization/actions/workflows/python-ci.yml)

## Overview
This project packs items into a bin using `py3dbp` and visualizes fitted items in 3D using Matplotlib.

It has been refactored from a single script into an installable package with:
- package and CLI entry points,
- dependency-safe `--help` behavior,
- modern `pyproject.toml` metadata with a compatibility fallback in `setup.py`,
- repository docs and contributor guidance,
- CI, build validation, and local test gates.

Technical notes and repository setup details are documented in `docs/PACKING_METHOD_AND_SETUP.md`.

## Structure
- `packaging_optimization/`: installable Python package
- `bin_packing_visualizer.py`: compatibility wrapper for the legacy script entry point
- `docs/`: technical documentation
- `tests/`: standard-library unit tests
- `pyproject.toml` and `setup.py`: package metadata

## Clone and Install
Standard installation:
```bash
git clone https://github.com/Mw1n23/PackagingOptimization.git
cd PackagingOptimization
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .[plot]
```

Development installation:
```bash
git clone https://github.com/Mw1n23/PackagingOptimization.git
cd PackagingOptimization
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[plot,dev]
```

## Run
Installed CLI:
```bash
packaging-optimization --help
```

Module entry point:
```bash
python -m packaging_optimization --help
```

Legacy script entry point:
```bash
python bin_packing_visualizer.py
```

Example with custom dimensions:
```bash
packaging-optimization --bin-width 155 --bin-height 53.5 --bin-depth 58.5 --num-items 100
```

## Tests
```bash
python -m unittest discover -s tests -q
```

## Build validation
```bash
python -m build
python -m twine check dist/*
```

## GitHub workflow
- CI runs on push and pull request across Python 3.10, 3.11, and 3.12.
- A separate build job validates wheel and sdist metadata.
- `CONTRIBUTING.md` defines the local gate.
- `CHANGELOG.md` tracks user-visible repository changes.
