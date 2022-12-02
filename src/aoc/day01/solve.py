"""Solution for day 1 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from pathlib import Path

import click
import click_pathlib
from pydantic import BaseModel


class Elf(BaseModel):
    """Elf representation."""

    calories: list[int]

    @property
    def total(self) -> int:
        """Determine sum of calories."""
        return sum(self.calories)


@click.command(name="day01")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 1."""
    elves = sorted(
        [
            Elf(calories=calories.split("\n"))
            for calories in path.read_text(encoding="utf-8").split("\n\n")
        ],
        key=lambda x: x.total if x else 0,
        reverse=True,
    )

    # pylint: disable=consider-using-generator
    print(f"Maximum number of calories: {elves[0].total}")
    print(f"Total of top three: {sum([t.total for t in elves[:3]])}")
