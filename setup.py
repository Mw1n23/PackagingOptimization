from pathlib import Path

from setuptools import find_packages, setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")


setup(
    name="packaging-optimization",
    version="0.1.0",
    description="Bin packing optimization and 3D visualization.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mw1n23",
    license="MIT",
    url="https://github.com/Mw1n23/PackagingOptimization",
    python_requires=">=3.10",
    packages=find_packages(include=["packaging_optimization", "packaging_optimization.*"]),
    include_package_data=True,
    install_requires=[
        "py3dbp>=1.8.4",
    ],
    extras_require={
        "plot": [
            "matplotlib>=3.5.0",
            "numpy>=1.21.0",
        ],
        "dev": ["pytest>=8"],
    },
    project_urls={
        "Source": "https://github.com/Mw1n23/PackagingOptimization",
        "Issues": "https://github.com/Mw1n23/PackagingOptimization/issues",
    },
    entry_points={
        "console_scripts": [
            "packaging-optimization=packaging_optimization.cli:main",
            "bin-packing-visualizer=packaging_optimization.cli:main",
        ]
    },
)
