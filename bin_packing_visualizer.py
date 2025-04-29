#!/usr/bin/env python3
"""
3D Bin Packing Visualizer

This script uses the py3dbp library to pack items into a storage unit and visualizes
the arrangement in a 3D plot using Matplotlib. It supports customizable storage units
and item configurations via command-line arguments.
"""

import argparse
from py3dbp import Packer, Bin, Item
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="3D Bin Packing Visualization")
    parser.add_argument('--bin-name', default='Tiefkühler', help='Name of the storage unit')
    parser.add_argument('--bin-width', type=float, default=155, help='Width of the storage unit')
    parser.add_argument('--bin-height', type=float, default=53.5, help='Height of the storage unit')
    parser.add_argument('--bin-depth', type=float, default=58.5, help='Depth of the storage unit')
    parser.add_argument('--bin-weight', type=float, default=600, help='Weight capacity of the storage unit')
    parser.add_argument('--num-items', type=int, default=100, help='Number of items to pack')
    parser.add_argument('--item-width', type=float, default=48, help='Width of each item')
    parser.add_argument('--item-height', type=float, default=28, help='Height of each item')
    parser.add_argument('--item-depth', type=float, default=3.5, help='Depth of each item')
    parser.add_argument('--item-weight', type=float, default=0.1, help='Weight of each item')
    return parser.parse_args()

def create_items(num_items, width, height, depth, weight):
    """Generate a list of items for packing."""
    try:
        return [Item(f'Akku{i}', width, height, depth, weight) for i in range(1, num_items + 1)]
    except Exception as e:
        logger.error(f"Error creating items: {e}")
        raise

def pack_items(bin_obj, items):
    """Pack items into the storage unit."""
    try:
        packer = Packer()
        packer.add_bin(bin_obj)
        for item in items:
            packer.add_item(item)
        packer.pack()
        return packer
    except Exception as e:
        logger.error(f"Error during packing: {e}")
        raise

def print_packing_results(packer):
    """Print details of fitted and unfitted items."""
    for b in packer.bins:
        logger.info(f"Bin: {b.string()}")
        logger.info("FITTED ITEMS:")
        for item in b.items:
            logger.info(f"  => {item.string()}")
        logger.info("UNFITTED ITEMS:")
        for item in b.unfitted_items:
            logger.info(f"  => {item.string()}")
        logger.info("***************************************************")

def get_random_color():
    """Generate a random color for visualization."""
    return np.random.rand(3,)

def add_box(ax, item, color):
    """Add a 3D box to the plot representing an item."""
    try:
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
    except Exception as e:
        logger.error(f"Error adding box to plot: {e}")
        raise

def visualize_packing(bin_obj):
    """Visualize packed items in a 3D plot."""
    try:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        color_mapping = {}

        for item in bin_obj.items:
            color = get_random_color()
            add_box(ax, item, color)
            color_mapping[item.name] = color

        # Create legend
        legend_labels = [plt.Line2D([0], [0], color=color, lw=4, label=name)
                         for name, color in color_mapping.items()]
        plt.legend(handles=legend_labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)

        # Set axis limits
        max_dim = max(bin_obj.width, bin_obj.height, bin_obj.depth) * 1.1
        ax.set_xlim([0, max_dim])
        ax.set_ylim([0, max_dim])
        ax.set_zlim([0, max_dim])

        # Labels and title
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.set_title(f'3D Visualization of Items in {bin_obj.name}')

        plt.show()
    except Exception as e:
        logger.error(f"Error during visualization: {e}")
        raise

def main():
    """Main function to run the packing and visualization."""
    args = parse_arguments()

    try:
        # Create storage unit
        storage_unit = Bin(args.bin_name, args.bin_width, args.bin_height,
                           args.bin_depth, args.bin_weight)
        logger.info(f"Created storage unit: {storage_unit.string()}")

        # Create items
        items = create_items(args.num_items, args.item_width, args.item_height,
                             args.item_depth, args.item_weight)
        logger.info(f"Created {args.num_items} items")

        # Pack items
        packer = pack_items(storage_unit, items)
        print_packing_results(packer)

        # Visualize
        visualize_packing(storage_unit)

    except Exception as e:
        logger.error(f"Program failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
