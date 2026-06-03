from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).parent
VERSION_NAMESPACE: dict[str, str] = {}
exec(
    (ROOT / "packaging_optimization" / "__init__.py").read_text(encoding="utf-8"),
    VERSION_NAMESPACE,
)


setup(
    name="packaging-optimization",
    version=VERSION_NAMESPACE["__version__"],
    description="Bin packing optimization and 3D visualization.",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Mw1n23",
    license="MIT",
    url="https://github.com/Mw1n23/PackagingOptimization",
    python_requires=">=3.10",
    packages=find_packages(include=["packaging_optimization", "packaging_optimization.*"]),
    include_package_data=True,
    install_requires=[
        "py3dbp>=1.1.2,<2",
    ],
    extras_require={
        "plot": [
            "matplotlib>=3.5.0",
            "numpy>=1.21.0",
        ],
        "dev": [
            "build>=1.2.1",
            "pytest>=8",
            "twine>=5.1.1",
        ],
    },
    project_urls={
        "Homepage": "https://github.com/Mw1n23/PackagingOptimization",
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
