"""Solution for day 3 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

import string
from functools import reduce
from pathlib import Path

import click
import click_pathlib
from pydantic import BaseModel


class Compartment(BaseModel):
    """A single compartment within a rucksack."""

    items: set[str]

    def __and__(self, other: Compartment) -> set[str]:
        """Determine overlap between two compartments."""
        return self.items.intersection(other.items)


def _to_priority(character: str) -> int:
    """Convert a character into a priority."""
    return string.ascii_letters.index(character) + 1


class Rucksack(BaseModel):
    """A rucksack carried by an elf."""

    items: list[str]

    @property
    def compartments(self) -> tuple[Compartment, Compartment]:
        """Split a list of characters into compartments."""
        return self._split_into_compartments(self.items)

    @property
    def priority(self) -> int:
        """Determine priority within a single rucksack."""
        overlap = self.compartments[0] & self.compartments[1]
        overlap_priorities = [_to_priority(c) for c in overlap]

        return sum(overlap_priorities)

    @staticmethod
    def _split_into_compartments(
        items: list[str], parts: int = 2
    ) -> tuple[Compartment, Compartment]:
        """Split line of text into two compartments."""
        length = len(items)

        # fmt: off
        return \
            Compartment(items=set(items[: int(length / parts)])),\
            Compartment(items=set(items[int(length / parts) :]))
        # fmt: on


class ElfGroup(BaseModel):
    """A group of elves who carry rucksacks."""

    rucksacks: list[Rucksack]

    @property
    def badge(self):
        """Determine group badge."""
        item_sets = [set(r.items) for r in self.rucksacks]

        return next(iter(reduce(lambda x, y: x & y, item_sets)))

    @property
    def priority(self) -> int:
        """Find priority of a group."""
        return _to_priority(self.badge)


@click.command(name="day03")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 3."""
    rucksacks = [
        Rucksack(items=list(r)) for r in path.read_text(encoding="utf-8").splitlines()
    ]

    groups = [
        ElfGroup(rucksacks=rucksacks[g : g + 3]) for g in range(0, len(rucksacks), 3)
    ]

    # pylint: disable=consider-using-generator
    print(f"[1] Sum of compartment priorities: {sum([r.priority for r in rucksacks])}")
    print(f"[2] Sum of group priorities: {sum([g.priority for g in groups])}")
