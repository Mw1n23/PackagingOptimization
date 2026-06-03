from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from typing import Any


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class BinSpec:
    name: str
    width: float
    height: float
    depth: float
    max_weight: float


@dataclass(frozen=True)
class ItemSpec:
    width: float
    height: float
    depth: float
    weight: float


@dataclass(frozen=True)
class PackingConfig:
    bin_spec: BinSpec
    item_spec: ItemSpec
    num_items: int
    plot: bool


@dataclass(frozen=True)
class PackingSummary:
    bin_name: str
    fitted_count: int
    unfitted_count: int
    fitted_names: list[str]
    unfitted_names: list[str]


def configure_logging() -> None:
    if logging.getLogger().handlers:
        return
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="3D bin packing optimization and visualization."
    )
    parser.add_argument("--bin-name", default="Tiefkuehler", help="Name of the storage unit.")
    parser.add_argument("--bin-width", type=float, default=155.0, help="Bin width.")
    parser.add_argument("--bin-height", type=float, default=53.5, help="Bin height.")
    parser.add_argument("--bin-depth", type=float, default=58.5, help="Bin depth.")
    parser.add_argument("--bin-weight", type=float, default=600.0, help="Bin weight capacity.")
    parser.add_argument("--num-items", type=int, default=100, help="Number of items to pack.")
    parser.add_argument("--item-width", type=float, default=48.0, help="Item width.")
    parser.add_argument("--item-height", type=float, default=28.0, help="Item height.")
    parser.add_argument("--item-depth", type=float, default=3.5, help="Item depth.")
    parser.add_argument("--item-weight", type=float, default=0.1, help="Item weight.")
    parser.add_argument(
        "--plot",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Render the 3D visualization with matplotlib.",
    )
    return parser


def parse_arguments(argv: list[str] | None = None) -> PackingConfig:
    args = build_parser().parse_args(argv)
    validate_positive(args.bin_width, "bin-width")
    validate_positive(args.bin_height, "bin-height")
    validate_positive(args.bin_depth, "bin-depth")
    validate_positive(args.bin_weight, "bin-weight")
    validate_positive(args.item_width, "item-width")
    validate_positive(args.item_height, "item-height")
    validate_positive(args.item_depth, "item-depth")
    validate_positive(args.item_weight, "item-weight")
    validate_positive_integer(args.num_items, "num-items")

    return PackingConfig(
        bin_spec=BinSpec(
            name=args.bin_name,
            width=args.bin_width,
            height=args.bin_height,
            depth=args.bin_depth,
            max_weight=args.bin_weight,
        ),
        item_spec=ItemSpec(
            width=args.item_width,
            height=args.item_height,
            depth=args.item_depth,
            weight=args.item_weight,
        ),
        num_items=args.num_items,
        plot=args.plot,
    )


def validate_positive(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")


def validate_positive_integer(value: int, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")


def load_packing_backend() -> tuple[type[Any], type[Any], type[Any]]:
    try:
        from py3dbp import Bin, Item, Packer
    except ImportError as exc:
        raise RuntimeError(
            "py3dbp is required for packing. Install the project dependencies first."
        ) from exc

    return Packer, Bin, Item


def load_plot_backend() -> tuple[Any, Any]:
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise RuntimeError(
            "matplotlib and numpy are required for plotting. Install the project dependencies first."
        ) from exc

    return plt, np


def create_items(
    item_cls: type[Any],
    num_items: int,
    item_spec: ItemSpec,
) -> list[Any]:
    return [
        item_cls(
            f"Akku{i}",
            item_spec.width,
            item_spec.height,
            item_spec.depth,
            item_spec.weight,
        )
        for i in range(1, num_items + 1)
    ]


def build_bin(bin_cls: type[Any], bin_spec: BinSpec) -> Any:
    return bin_cls(
        bin_spec.name,
        bin_spec.width,
        bin_spec.height,
        bin_spec.depth,
        bin_spec.max_weight,
    )


def pack_items(bin_obj: Any, items: list[Any], packer_cls: type[Any]) -> Any:
    packer = packer_cls()
    packer.add_bin(bin_obj)
    for item in items:
        packer.add_item(item)
    packer.pack()
    return packer


def summarize_packing(bin_obj: Any) -> PackingSummary:
    fitted_names = [item.name for item in bin_obj.items]
    unfitted_names = [item.name for item in bin_obj.unfitted_items]
    return PackingSummary(
        bin_name=bin_obj.name,
        fitted_count=len(fitted_names),
        unfitted_count=len(unfitted_names),
        fitted_names=fitted_names,
        unfitted_names=unfitted_names,
    )


def print_packing_results(bin_obj: Any) -> PackingSummary:
    summary = summarize_packing(bin_obj)
    LOGGER.info("Bin: %s", bin_obj.string())
    LOGGER.info("FITTED ITEMS: %s", summary.fitted_count)
    for item in bin_obj.items:
        LOGGER.info("  => %s", item.string())
    LOGGER.info("UNFITTED ITEMS: %s", summary.unfitted_count)
    for item in bin_obj.unfitted_items:
        LOGGER.info("  => %s", item.string())
    LOGGER.info("***************************************************")
    return summary


def get_deterministic_color(index: int) -> tuple[float, float, float]:
    palette = [
        (0.12, 0.47, 0.71),
        (1.0, 0.5, 0.05),
        (0.17, 0.63, 0.17),
        (0.84, 0.15, 0.16),
        (0.58, 0.4, 0.74),
        (0.55, 0.34, 0.29),
        (0.89, 0.47, 0.76),
        (0.5, 0.5, 0.5),
        (0.74, 0.74, 0.13),
        (0.09, 0.75, 0.81),
    ]
    return palette[index % len(palette)]


def add_box(ax: Any, item: Any, color: tuple[float, float, float], np: Any) -> None:
    pos = np.array(item.position, dtype=float)
    dim = np.array(item.get_dimension(), dtype=float)

    xx, yy = np.meshgrid([pos[0], pos[0] + dim[0]], [pos[1], pos[1] + dim[1]])
    ax.plot_surface(xx, yy, np.full_like(xx, pos[2]), color=color, alpha=0.5)
    ax.plot_surface(xx, yy, np.full_like(xx, pos[2] + dim[2]), color=color, alpha=0.5)

    yy, zz = np.meshgrid([pos[1], pos[1] + dim[1]], [pos[2], pos[2] + dim[2]])
    ax.plot_surface(np.full_like(yy, pos[0]), yy, zz, color=color, alpha=0.5)
    ax.plot_surface(np.full_like(yy, pos[0] + dim[0]), yy, zz, color=color, alpha=0.5)

    xx, zz = np.meshgrid([pos[0], pos[0] + dim[0]], [pos[2], pos[2] + dim[2]])
    ax.plot_surface(xx, np.full_like(xx, pos[1]), zz, color=color, alpha=0.5)
    ax.plot_surface(xx, np.full_like(xx, pos[1] + dim[1]), zz, color=color, alpha=0.5)


def visualize_packing(bin_obj: Any) -> None:
    plt, np = load_plot_backend()
    figure = plt.figure(figsize=(10, 10))
    axis = figure.add_subplot(111, projection="3d")
    color_mapping: dict[str, tuple[float, float, float]] = {}

    for index, item in enumerate(bin_obj.items):
        color = get_deterministic_color(index)
        add_box(axis, item, color, np)
        color_mapping[item.name] = color

    legend_labels = [
        plt.Line2D([0], [0], color=color, lw=4, label=name)
        for name, color in color_mapping.items()
    ]
    if legend_labels:
        plt.legend(
            handles=legend_labels,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.05),
            fancybox=True,
            shadow=True,
            ncol=5,
        )

    max_dim = max(bin_obj.width, bin_obj.height, bin_obj.depth) * 1.1
    axis.set_xlim([0, max_dim])
    axis.set_ylim([0, max_dim])
    axis.set_zlim([0, max_dim])
    axis.set_xlabel("X axis")
    axis.set_ylabel("Y axis")
    axis.set_zlabel("Z axis")
    axis.set_title(f"3D Visualization of Items in {bin_obj.name}")
    plt.tight_layout()
    plt.show()


def run(config: PackingConfig) -> PackingSummary:
    packer_cls, bin_cls, item_cls = load_packing_backend()
    storage_unit = build_bin(bin_cls, config.bin_spec)
    LOGGER.info("Created storage unit: %s", storage_unit.string())

    items = create_items(item_cls, config.num_items, config.item_spec)
    LOGGER.info("Created %s items", config.num_items)

    packer = pack_items(storage_unit, items, packer_cls)
    if not packer.bins:
        raise RuntimeError("Packing backend returned no bins.")

    packed_bin = packer.bins[0]
    summary = print_packing_results(packed_bin)

    if config.plot:
        visualize_packing(packed_bin)

    return summary


def main(argv: list[str] | None = None) -> int:
    try:
        configure_logging()
        config = parse_arguments(argv)
        run(config)
    except Exception as exc:
        LOGGER.error("Program failed: %s", exc)
        return 1
    return 0
