# Changelog

## Unreleased

- Fixed the 3D visualization: it stopped with "unsupported operand type(s) for *: 'decimal.Decimal' and 'float'" because `py3dbp` stores dimensions as `Decimal`, so every default run ended with an error.
- Unexpected errors keep their traceback; only invalid arguments and missing dependencies are reported as a one-line error.
- `setup.py` is now the compatibility shim the 0.1.1 notes describe; all metadata lives in `pyproject.toml`.
- License metadata uses the SPDX form required by setuptools from February 2027.
- The package version matches the changelog (0.1.1).
- CI tests the plot path as well, caches pip downloads and uses read-only permissions.

## 0.1.1

- Fixed the package dependency constraint for `py3dbp` so GitHub Actions and normal `pip install .` runs can resolve the runtime backend from PyPI.
- Moved package metadata into `pyproject.toml` and reduced `setup.py` to a compatibility shim.
- Expanded CI to test multiple Python versions and validate wheel/sdist builds.
- Removed the import-time logging side effect from the CLI module.

## 0.1.0

- Refactored the project from a single script into an installable Python package.
- Added console entry points for package and legacy-style execution.
- Deferred heavy imports so help text, tests, and packaging checks do not fail before dependencies are installed.
- Added repository documentation, contribution guidance, GitHub templates, and CI updates.
