# Changelog

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
