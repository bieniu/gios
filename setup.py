#!/usr/bin/env python
from setuptools import setup


setup(
    name="gios",
    version="0.1.0",
    author="Maciej Bieniek",
    author_email="maciej.bieniek@gmail.com",
    description="Python wrapper for getting air quality data from GIOŚ servers.",
    include_package_data=True,
    url="https://github.com/bieniu/gios",
    license="Apache 2",
    packages=["gios"],
    python_requires=">=3.6",
    install_requires=["aiohttp"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    setup_requires=("pytest-runner"),
    tests_require=(
        "asynctest",
        "pytest-cov",
        "pytest-asyncio",
        "pytest-trio",
        "pytest-tornasync",
    ),
)
