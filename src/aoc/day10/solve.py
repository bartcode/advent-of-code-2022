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

CRT_WIDTH = 40
CRT_HEIGHT = 7
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
    drawing: dict[int, str] = {i: "" for i in range(CRT_HEIGHT)}
    sprite_position: int = 0
    current_pixel: int = 0
    pixel_value: int = 1

    def process(self, instruction: Instruction) -> None:
        """Process instruction."""
        for _ in range(instruction.type.value):
            self.current_cycle += 1
            if self.current_cycle == 20 or (self.current_cycle + 20) % 40 == 0:
                self.cycles.append(self.value * self.current_cycle)
        else:
            self.value += instruction.value

    def draw(self, instruction: Instruction) -> None:
        """Draw instructions on CRT screen."""
        index = 0

        for index in range(instruction.type.value):
            position = self.current_cycle % 40
            self.drawing[self.current_cycle // 40] += "#" if position in range(self.pixel_value - 1, self.pixel_value + 2) else "."
            self.current_cycle += 1
            if index == 0:
                logger.debug("Start cycle   %d: begin executing %s %d", self.current_cycle, instruction.type.name, instruction.value)
                logger.debug("During cycle  %d: CRT draws pixel in position %d", self.current_cycle, position)
                logger.debug("Current CRT row: %s", self.drawing[self.current_cycle // 40])
                logger.debug("")
        else:
            self.pixel_value += instruction.value

            if index > 0:
                logger.debug("During cycle  %d: CRT draws pixel in position %d", self.current_cycle, self.current_cycle % 40)
                logger.debug("Current CRT row: %s", self.drawing[self.current_cycle // 40])
                logger.debug("End of cycle  %d: finish executing %s %d (Register X is now %d)", self.current_cycle,
                            instruction.type.name, instruction.value, self.pixel_value)
                sprite = "." * CRT_WIDTH
                sprite = sprite[:self.pixel_value - 1] + "###" + sprite[self.pixel_value + 2:]
                logger.debug("Sprite position: %s", sprite)
                logger.debug("")

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

    return Instruction(type=getattr(InstructionType, details[0].upper()), value=details[1] if len(details) > 1 else 0)


@click.command(name="day10")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 10."""
    instructions = [_parse_instruction(l) for l in path.read_text().splitlines() if l]
    program = Program()

    for instruction in instructions:
        program.process(instruction)
    print(f"[1] Signal strength: {program.signal_strength}")

    crt = Program()
    for instruction in instructions:
        crt.draw(instruction)

    print(f"[2] CRT output:\n{crt.drawing_output}")
