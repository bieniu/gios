#!/usr/bin/env python
from setuptools import find_namespace_packages, setup


setup(
    name="gios",
    version="0.0.2",
    author="Maciej Bieniek",
    author_email="maciej.bieniek@gmail.com",
    description="Python wrapper for getting air quality data from GIOŚ servers.",
    include_package_data=True,
    url="https://github.com/bieniu/gios",
    license="Apache 2",
    packages=["gios"],
    python_requires=">=3.7.0",
    install_requires=["aiohttp"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
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
