from pathlib import Path


def test_visualizer_compiles() -> None:
    source = Path("bin_packing_visualizer.py").read_text(encoding="utf-8")
    compile(source, "bin_packing_visualizer.py", "exec")
