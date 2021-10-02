#!/usr/bin/env python3
from setuptools import setup


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", "r", encoding="utf-8") as file:
    install_requires=list(val.strip() for val in file.readlines())

with open("requirements-test.txt", "r", encoding="utf-8") as file:
    tests_require=list(val.strip() for val in file.readlines())

setup(
    name="gios",
    version="2.1.0",
    author="Maciej Bieniek",
    description="Python wrapper for getting air quality data from GIOŚ servers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/bieniu/gios",
    license="Apache-2.0 License",
    packages=["gios"],
    package_data={"gios": ["py.typed"]},
    python_requires=">=3.8",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Typing :: Typed",
    ],
    setup_requires=("pytest-runner"),
    tests_require=tests_require,
)
