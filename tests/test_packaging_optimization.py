import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from packaging_optimization import cli


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "bin_packing_visualizer.py"
CLI_MODULE_PATH = REPO_ROOT / "packaging_optimization" / "cli.py"


class PackagingOptimizationTests(unittest.TestCase):
    def test_cli_module_compiles(self) -> None:
        source = CLI_MODULE_PATH.read_text(encoding="utf-8")
        compile(source, str(CLI_MODULE_PATH), "exec")

    def test_module_help_works_without_dependencies(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "packaging_optimization", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("3D bin packing optimization and visualization", result.stdout)

    def test_legacy_script_help_works_without_dependencies(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("3D bin packing optimization and visualization", result.stdout)

    def test_parse_arguments_returns_config(self) -> None:
        config = cli.parse_arguments(
            [
                "--bin-name",
                "TestBin",
                "--bin-width",
                "120",
                "--bin-height",
                "40",
                "--bin-depth",
                "60",
                "--bin-weight",
                "100",
                "--num-items",
                "10",
                "--item-width",
                "20",
                "--item-height",
                "10",
                "--item-depth",
                "5",
                "--item-weight",
                "1",
                "--no-plot",
            ]
        )

        self.assertEqual(config.bin_spec.name, "TestBin")
        self.assertEqual(config.num_items, 10)
        self.assertFalse(config.plot)

    def test_main_returns_error_when_backend_missing(self) -> None:
        with mock.patch.object(
            cli,
            "load_packing_backend",
            side_effect=RuntimeError("py3dbp missing"),
        ), mock.patch.object(cli.LOGGER, "error"):
            exit_code = cli.main(["--no-plot"])

        self.assertEqual(exit_code, 1)

    def test_run_returns_summary_with_mocked_backend(self) -> None:
        class FakeItem:
            def __init__(self, name: str, width: float, height: float, depth: float, weight: float):
                self.name = name
                self.width = width
                self.height = height
                self.depth = depth
                self.weight = weight
                self.position = (0, 0, 0)

            def string(self) -> str:
                return self.name

            def get_dimension(self):
                return (self.width, self.height, self.depth)

        class FakeBin:
            def __init__(self, name: str, width: float, height: float, depth: float, max_weight: float):
                self.name = name
                self.width = width
                self.height = height
                self.depth = depth
                self.max_weight = max_weight
                self.items = []
                self.unfitted_items = []

            def string(self) -> str:
                return self.name

        class FakePacker:
            def __init__(self):
                self.bins = []
                self._bin = None
                self._items = []

            def add_bin(self, bin_obj):
                self._bin = bin_obj
                self.bins.append(bin_obj)

            def add_item(self, item):
                self._items.append(item)

            def pack(self):
                self._bin.items = self._items[:2]
                self._bin.unfitted_items = self._items[2:]

        config = cli.PackingConfig(
            bin_spec=cli.BinSpec("TestBin", 100.0, 50.0, 40.0, 500.0),
            item_spec=cli.ItemSpec(10.0, 5.0, 4.0, 1.0),
            num_items=3,
            plot=False,
        )

        with mock.patch.object(
            cli,
            "load_packing_backend",
            return_value=(FakePacker, FakeBin, FakeItem),
        ), mock.patch.object(cli.LOGGER, "info"):
            summary = cli.run(config)

        self.assertEqual(summary.bin_name, "TestBin")
        self.assertEqual(summary.fitted_count, 2)
        self.assertEqual(summary.unfitted_count, 1)


if __name__ == "__main__":
    unittest.main()
