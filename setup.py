"""Setup module for gios."""
from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "3.2.2"

setup(
    name="gios",
    version=VERSION,
    author="Maciej Bieniek",
    description="Python wrapper for getting air quality data from GIOŚ servers.",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/bieniu/gios",
    license="Apache-2.0 License",
    packages=["gios"],
    package_data={"gios": ["py.typed"]},
    python_requires=">=3.11",
    install_requires=["aiohttp>=3.7.0", "dacite>=1.7.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Typing :: Typed",
    ],
)
