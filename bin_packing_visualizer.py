#!/usr/bin/env python3
"""Compatibility wrapper for the legacy entry script."""

from packaging_optimization.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
