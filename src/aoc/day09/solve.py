"""Solution for day 9 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods,invalid-name
from __future__ import annotations

import logging
from pathlib import Path

import click
import click_pathlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Snake:
    """A snake."""

    x: int = 0
    y: int = 0
    tail: list[list[int]]
    visited: set[tuple[int, int]]

    def __init__(self, tail_length: int = 1):
        """Initialize snake with a certain tail length."""
        self.visited = set()
        self.tail_length = tail_length
        self.tail = [[0, 0] for _ in range(self.tail_length)]

    def move(self, instruction: str):
        """Move the head of the snake in a certain direction."""
        direction, steps = instruction.split(" ")
        steps = int(steps)

        for _ in range(steps):
            if direction == "L":
                self.x -= 1
            elif direction == "R":
                self.x += 1
            elif direction == "U":
                self.y -= 1
            else:
                self.y += 1

            previous_x = self.x
            previous_y = self.y

            for index in range(self.tail_length):
                tail_y, tail_x = self.tail[index]

                if abs(previous_y - tail_y) == 2 or abs(previous_x - tail_x) == 2:
                    tail_y += (
                        1 if previous_y > tail_y else 0 if previous_y == tail_y else -1
                    )
                    tail_x += (
                        1 if previous_x > tail_x else 0 if previous_x == tail_x else -1
                    )

                self.tail[index] = [tail_y, tail_x]
                previous_x, previous_y = tuple(self.tail[index])

            self.visited.add((self.tail[-1][0], self.tail[-1][1]))

    def unique_tail_positions(self) -> int:
        """Unique positions of the tail."""
        return len(self.visited)


@click.command(name="day09")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 9."""
    snake = Snake(1)
    for instruction in path.read_text().splitlines():
        snake.move(instruction)
    print(f"[1] Tail positions: {snake.unique_tail_positions()}")

    snake = Snake(9)
    for instruction in path.read_text().splitlines():
        snake.move(instruction)
    print(f"[2] Tail position of the long end: {snake.unique_tail_positions()}")
