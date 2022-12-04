"""Solution for day 4 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import click
import click_pathlib


@dataclass
class Elf:
    """Represent a single elf."""

    range_identifier: str

    @property
    def range(self) -> set[int]:
        """Find range of assignments for elf."""
        range_boundaries = [int(i) for i in self.range_identifier.split("-")]
        return set(range(range_boundaries[0], range_boundaries[1] + 1))

    def __repr__(self) -> str:
        """Represent an elf."""
        return f"Elf(range={self.range_identifier})"

    def __and__(self, other: Elf) -> bool:
        """Determine whether one elf's assignments overlap with another."""
        return self.range <= other.range or other.range <= self.range

    def __or__(self, other: Elf) -> bool:
        """Determine whether one elf's assignments overlap with another."""
        return bool(self.range.intersection(other.range))


@dataclass
class CampPair:
    """A pair of elves within the camp."""

    raw_data: str

    @property
    def elves(self) -> list[Elf]:
        """Elves within a camp pair."""
        return [Elf(range_identifier=e) for e in self.raw_data.split(",")]

    def __repr__(self) -> str:
        """Represent a pair."""
        return f"CampPair(elves={str(self.elves)})"

    @property
    def full_overlap(self) -> bool:
        """Determine whether there's full overlap between two elves."""
        elves = self.elves
        return elves[0] & elves[1]

    @property
    def overlap(self) -> bool:
        """Determine whether there's some overlap between two elves."""
        elves = self.elves
        return elves[0] | elves[1]


@click.command(name="day04")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 4."""
    pairs = [
        CampPair(raw_data=p) for p in path.read_text(encoding="utf-8").splitlines() if p
    ]

    # fmt: off
    # pylint: disable=consider-using-generator,line-too-long
    print(f"[1] Full overlapping pairs: {sum([1 for v in pairs if v.full_overlap])} out of {len(pairs)}.")
    print(f"[2] Partially overlapping pairs: {sum([1 for v in pairs if v.overlap])} out of {len(pairs)}.")
    # fmt: on
