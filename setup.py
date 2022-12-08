"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_namespace_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("./src/aoc/__init__.py") as fp:
    # pylint: disable=W0122
    exec(fp.read(), VERSION)

setup(
    name="advent_of_code",
    author="Bart Hazen",
    description="Advent of Code 2022",
    version=VERSION.get("__version__", "0.0.1"),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
        "click~=8.1",
        "coloredlogs~=15.0",
        "pydantic~=1.10",
        "click-pathlib==2020.3.13.0",
        "numpy~=1.23",
    ],
    entry_points={
        "console_scripts": [
            "aoc=aoc.__main__:main",
            "advent=aoc.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)