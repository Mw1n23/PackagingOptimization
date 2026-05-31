# 3D Bin Packing Visualization

## Overview
This project packs items into a bin using `py3dbp` and visualizes fitted items in 3D using Matplotlib.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python bin_packing_visualizer.py
```

Example with custom dimensions:
```bash
python bin_packing_visualizer.py --bin-width 155 --bin-height 53.5 --bin-depth 58.5 --num-items 100
```

## Tests
```bash
pytest -q
```
