# Packing Method and Repository Setup

## Why this repository exists
This repository explores how many identically sized items can be placed inside a constrained storage volume using a 3D bin packing algorithm and an optional 3D visualization.

The project started as a single script. It is now structured as an installable package so it can be cloned, installed, tested, and published to GitHub in a predictable way.

## Current implementation
The runtime entry point is `packaging_optimization.cli`.

### Core flow
1. Parse CLI arguments into a typed configuration.
2. Build one bin definition and a repeated set of item definitions.
3. Run the `py3dbp` packing backend.
4. Print a packing summary to the console.
5. Optionally render the fitted items with Matplotlib in 3D.

### Key design choices
- Import `py3dbp`, `matplotlib`, and `numpy` lazily.
  This allows `--help`, imports, tests, and packaging checks to work even when optional runtime dependencies are not installed yet.
- Keep the legacy `bin_packing_visualizer.py` script as a compatibility wrapper.
- Use deterministic colors for plotted items so repeated runs do not produce visually noisy screenshots.

## Install modes

### Standard user install
```bash
git clone https://github.com/Mw1n23/PackagingOptimization.git
cd PackagingOptimization
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .[plot]
```

### Development install
```bash
git clone https://github.com/Mw1n23/PackagingOptimization.git
cd PackagingOptimization
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[plot]
```

## CLI entry points
- `packaging-optimization`
- `bin-packing-visualizer`
- `python -m packaging_optimization`

## Local gate
Run before pushing:
```bash
python -m unittest discover -s tests -q
python -m packaging_optimization --help
python bin_packing_visualizer.py --help
```

## Limitations
- The current CLI models one repeated item type. It does not yet support mixed item catalogs.
- Visualization is informative, not physically validated beyond the packing backend result.
- Rendering many items can become visually dense and harder to inspect.
