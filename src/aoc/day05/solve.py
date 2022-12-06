"""Solution for day 5 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

from pathlib import Path

import click
import click_pathlib
from pydantic import BaseModel


class Stack(BaseModel):
    """A stack of crates."""

    crates: list[str] = []


class Instructions(BaseModel):
    """A set of instructions for a move."""

    items: int
    start: int
    towards: int


class Structure(BaseModel):
    """A structure that contains stacks of crates."""

    stacks: list[Stack] = []

    @staticmethod
    def _to_instructions(instruction: str) -> Instructions:
        """Convert instructions into parameters."""
        _, items, __, start, ___, towards = instruction.split(" ")
        return Instructions(
            items=int(items), start=int(start) - 1, towards=int(towards) - 1
        )

    def single_move(self, instruction: str) -> Structure:
        """Move a single crate at the same time."""
        instructions = self._to_instructions(instruction)

        for _ in range(instructions.items):
            item = self.stacks[instructions.start].crates[0]
            self.stacks[instructions.towards].crates = [item] + self.stacks[
                instructions.towards
            ].crates
            del self.stacks[instructions.start].crates[0]
        return self

    def multi_move(self, instruction: str) -> Structure:
        """Move multiple crates at the same time."""
        instructions = self._to_instructions(instruction)
        crates = self.stacks[instructions.start].crates[0 : instructions.items]
        self.stacks[instructions.towards].crates = (
            list(crates) + self.stacks[instructions.towards].crates
        )
        del self.stacks[instructions.start].crates[0 : instructions.items]

        return self


def _parse_stacks(data: str) -> Structure:
    """Parse string structure into Structure object."""
    columns = int(data[-1].strip().split(" ")[-1])
    rows = len(data) - 1

    base_structure = Structure(stacks=[])

    for column in range(columns):
        base_structure.stacks.append(Stack())

    for row in reversed(range(rows)):
        for column in range(columns):
            try:
                crate_name = data[row][1 + column * 4]
                if crate_name.strip():
                    base_structure.stacks[column].crates.insert(0, crate_name)
            except IndexError:
                pass

    return base_structure


@click.command(name="day05")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 5."""
    structure_data, moves = path.read_text().split("\n\n")
    single_move_structure = _parse_stacks(structure_data.split("\n"))

    for move in moves.splitlines():
        single_move_structure.single_move(instruction=move)

    print(
        f"[1] Top crates: {''.join([s.crates[0] for s in single_move_structure.stacks])}"
    )

    multi_move_structure = _parse_stacks(structure_data.split("\n"))
    for move in moves.splitlines():
        multi_move_structure.multi_move(instruction=move)

    print(
        f"[2] Top crates: {''.join([s.crates[0] for s in multi_move_structure.stacks])}"
    )
