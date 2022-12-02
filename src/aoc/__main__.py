"""CLI to solve Advent of Code 2022 challenges."""
import importlib
import logging
from pathlib import Path

import click
import coloredlogs
from click import Group
from setuptools import find_packages

logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO")


def add_solvers(base_cli: Group) -> None:
    """Dynamically add groups to main CLI."""
    solutions = [p for p in find_packages(str(Path(__file__).parent)) if "day" in p]

    for solution in solutions:
        cli = importlib.import_module(f"{__package__}.{solution}.solve")
        base_cli.add_command(cli.main)


@click.group()
def main() -> None:
    """Program to solve Advent of Code 2022 challenges."""


add_solvers(main)

if __name__ == "__main__":
    main()
