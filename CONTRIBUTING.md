# Contributing

## Development setup
```bash
git clone https://github.com/Mw1n23/PackagingOptimization.git
cd PackagingOptimization
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[plot,dev]
```

## Local validation
Run the repository gate before opening a pull request:
```bash
python -m unittest discover -s tests -q
python -m packaging_optimization --help
python bin_packing_visualizer.py --help
python -m build
python -m twine check dist/*
```

## Change scope
- Keep the CLI stable unless there is a clear usability gain.
- Prefer deterministic behavior over visual randomness.
- Keep the legacy wrapper script working unless it is explicitly removed in a breaking release.
- Avoid mixing packaging work and algorithm work in the same pull request unless they are tightly related.

## Pull request notes
- Describe any change to packing behavior or output.
- Mention whether visualization behavior changed.
- Include the command(s) you used for validation.
