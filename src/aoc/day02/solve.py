"""Solution for day 2 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

from enum import Enum, auto
from pathlib import Path

import click
import click_pathlib
from pydantic.main import BaseModel


class Hand(Enum):
    """Potential hands to play."""

    ROCK: int = 1
    PAPER: int = 2
    SCISSORS: int = 3

    def __and__(self, result: Outcome):
        """The required hand given a certain outcome."""
        # pylint: disable=too-many-return-statements
        match (result, self):
            case (result.DRAW, _):
                return self
            case (result.WIN, self.ROCK):
                return Hand.PAPER
            case (result.WIN, self.PAPER):
                return Hand.SCISSORS
            case (result.WIN, self.SCISSORS):
                return Hand.ROCK
            case (result.LOSS, self.ROCK):
                return Hand.SCISSORS
            case (result.LOSS, self.PAPER):
                return Hand.ROCK
            case (result.LOSS, self.SCISSORS):
                return Hand.PAPER

    def __gt__(self, other: Hand) -> bool:
        """Determine whether one hand is better than another."""
        match (self, other):
            # fmt: off
            case (self.ROCK, self.SCISSORS) | (self.SCISSORS, self.PAPER) | (self.PAPER, self.ROCK):
                return True
            case _:
                return False
            # fmt: on

    def __lt__(self, other: Hand) -> bool:
        """Determine whether one hand is worse than another."""
        return not self > other


class Outcome(Enum):
    """Possible outcomes of a single round."""

    LOSS: int = 0
    DRAW: int = 3
    WIN: int = 6


class Round(BaseModel):
    """A single round with two hands."""

    opponent: Hand
    choice: Hand

    @property
    def points(self) -> int:
        """Get points for a single round."""
        if self.choice > self.opponent:
            return Outcome.WIN.value + self.choice.value
        if self.choice == self.opponent:
            return Outcome.DRAW.value + self.choice.value
        return Outcome.LOSS.value + self.choice.value


class Match(BaseModel):
    """Represent a set of rounds within a match."""

    rounds: list[Round]

    @property
    def points_total(self):
        """Determine points for entire match."""
        # pylint: disable=consider-using-generator
        return sum([r.points for r in self.rounds])


class DecryptionMode(Enum):
    """Decryption mode of the second column."""

    HANDS = auto()
    OUTCOME = auto()


hand_mapping: dict[str, Hand] = {
    "A": Hand.ROCK,
    "X": Hand.ROCK,
    "B": Hand.PAPER,
    "Y": Hand.PAPER,
    "C": Hand.SCISSORS,
    "Z": Hand.SCISSORS,
}

outcome_mapping: dict[str, Outcome] = {
    "X": Outcome.LOSS,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}


def _to_round(line: str, mode: DecryptionMode) -> Round:
    """Convert a single line to a round."""
    opponent, choice = line.split(" ")

    if mode == DecryptionMode.HANDS:
        return Round(opponent=hand_mapping[opponent], choice=hand_mapping[choice])
    # if mode == DecryptionMode.OUTCOME:
    return Round(
        opponent=hand_mapping[opponent],
        choice=(hand_mapping[opponent] & outcome_mapping[choice]),
    )


@click.command(name="day02")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 2."""
    hand_decryption = Match(
        rounds=[
            _to_round(p, DecryptionMode.HANDS)
            for p in path.read_text(encoding="utf-8").splitlines()
            if p
        ]
    )
    outcome_decryption = Match(
        rounds=[
            _to_round(p, DecryptionMode.OUTCOME)
            for p in path.read_text(encoding="utf-8").splitlines()
            if p
        ]
    )

    # fmt: off
    print(f"[1] Total points with hand decryption: {hand_decryption.points_total}.")
    print(f"[2] Total points with outcome decryption: {outcome_decryption.points_total}.")
    # fmt: on
