"""Solution for day 9 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

import logging
import math
from pathlib import Path

import click
import click_pathlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Snake:
    """A snake."""
    tail_snake: Snake | None = None
    head: tuple[int, int]
    tail: tuple[int, int]
    visited: set[tuple[int, int]]

    def __init__(self, tail_length: int = 1):
        """Initialize snake with a certain tail length."""
        self.tail_length = tail_length
        self.head = (0, 0)
        self.tail = (0, 0)
        self.visited = set()
        self.tail_length = tail_length

        if self.tail_length > 1:
            self.tail_snake = Snake(tail_length=self.tail_length - 1)

    @property
    def tail_end(self) -> Snake:
        """Get the end of the snake."""
        if self.tail_snake:
            return self.tail_snake.tail_end
        return self

    def move(self, instruction: str):
        """Move the head of the snake in a certain direction."""
        direction, size = instruction.split(" ")
        direction_mapping = {
            "U": self.up,
            "R": self.right,
            "D": self.down,
            "L": self.left,
        }
        for _ in range(int(size)):
            direction_mapping[direction]()

    def update_tails(self) -> None:
        """Update subtails."""
        if self.tail_snake:
            self.tail_snake.head = self.tail
            self.tail_snake.move_tail()

    def move_tail(self) -> None:
        """Move tail in the direction of the head."""
        # Tail is 2 places too far on the right or left compared to the head, and must move accordingly.
        if abs(self.tail[0] - self.head[0]) > 1:
            if self.tail[1] != self.head[1]:  # Diagonal
                self.tail = (self.tail[0], self.head[1])

            self.tail = (
                self.tail[0] + int(math.copysign(1, self.head[0] - self.tail[0])),
                self.tail[1],
            )

        # Tail is 2 places higher/lower than the head, and must move accordingly.
        if abs(self.tail[1] - self.head[1]) > 1:
            if self.tail[0] != self.head[0]:  # Diagonal
                self.tail = (self.head[0], self.tail[1])

            self.tail = (
                self.tail[0],
                self.tail[1] + int(math.copysign(1, self.head[1] - self.tail[1])),
            )
        if self.tail_length == 1:
            print(self.tail[0], self.tail[1])

        self.visited.add(self.tail)
        self.update_tails()

    def unique_tail_positions(self) -> int:
        """Find number of unique tail positions."""
        return len(self.visited)

    def up(self, direction: int = 1) -> None:
        """A single move upwards or downwards."""
        self.head = (
            self.head[0],
            self.head[1] + int(math.copysign(1, direction))
        )
        self.move_tail()

    def right(self, direction: int = 1) -> None:
        """A single move to the right or left."""
        self.head = (
            self.head[0] + int(math.copysign(1, direction)),
            self.head[1]
        )
        self.move_tail()

    def down(self) -> None:
        """A single move downwards."""
        self.up(-1)

    def left(self) -> None:
        """A single move to the left."""
        self.right(-1)


@click.command(name="day09")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 9."""
    snake = Snake(tail_length=9)
    for instruction in path.read_text().splitlines():
        snake.move(instruction)
    print(f"[1] Tail positions: {snake.unique_tail_positions()}")

    # Should be 2273
    print(f"[2] Tail position of the long end: {snake.tail_end.unique_tail_positions()}")
