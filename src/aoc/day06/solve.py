"""Solution for day 6 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

from pathlib import Path
from typing import Iterator

import click
import click_pathlib


def find_marker(message: Iterator[str], minimum_signals: int) -> int:
    """Find the marker within a message."""
    # fmt: off
    window = []
    for index, value in enumerate(message):
        window.append(value)
        if index + 1 > minimum_signals \
                and len(window[-minimum_signals:]) == len(set(window[-minimum_signals:])):
            return index + 1
    return 0
    # fmt: on


@click.command(name="day06")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 5."""
    input_text = iter(path.read_text())
    print(f"[1] First start-of-packet: {find_marker(input_text, 4)}.")

    input_text = iter(path.read_text())
    print(f"[2] First start-of-packet: {find_marker(input_text, 14)}.")
