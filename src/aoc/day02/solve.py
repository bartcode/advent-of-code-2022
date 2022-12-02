"""Fix for day 2 of Advent of Code."""
from pathlib import Path

import click
import click_pathlib
from pydantic import BaseModel


class Round(BaseModel):


@click.command(name="day02")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 2."""

