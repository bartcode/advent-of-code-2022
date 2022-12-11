"""Solution for day 10 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods,invalid-name
from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path

import click
import click_pathlib
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CRT_HEIGHT = 6
SPRITE_WIDTH = 3


class InstructionType(Enum):
    """Available instruction types."""

    NOOP: int = 1
    ADDX: int = 2


class Instruction(BaseModel):
    """Instruction to a program."""

    type: Enum
    value: int


class Program(BaseModel):
    """Represent a program."""

    current_cycle: int = 0
    value: int = 1

    cycles: list[int] = []
    drawing: dict[int, str] = {i: "" for i in range(CRT_HEIGHT + 1)}

    def process(self, instruction: Instruction) -> None:
        """Process instruction."""
        for _ in range(instruction.type.value):
            self.drawing[self.current_cycle // 40] += (
                "#"
                if self.current_cycle % 40 in range(self.value - 1, self.value + 2)
                else "."
            )

            self.current_cycle += 1

            if self.current_cycle == 20 or (self.current_cycle + 20) % 40 == 0:
                self.cycles.append(self.value * self.current_cycle)

        self.value += instruction.value

    @property
    def drawing_output(self) -> str:
        """Output of the drawing on the screen."""
        return "\n".join(self.drawing.values())

    @property
    def signal_strength(self) -> int:
        """Determine total signal strength."""
        return sum(self.cycles)


def _parse_instruction(instruction: str) -> Instruction:
    """Parse line with raw instructions into Instruction object."""
    details = instruction.split(" ")

    return Instruction(
        type=getattr(InstructionType, details[0].upper()),
        value=details[1] if len(details) > 1 else 0,
    )


@click.command(name="day10")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 10."""
    instructions = [_parse_instruction(l) for l in path.read_text().splitlines() if l]
    program = Program()

    for instruction in instructions:
        program.process(instruction)
    print(f"[1] Signal strength: {program.signal_strength}")
    print(f"[2] CRT output:\n{program.drawing_output}")
