"""Solution for day 11 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods,invalid-name
from __future__ import annotations

import logging
import operator
from functools import reduce
from pathlib import Path

import click
import click_pathlib
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


class ItemCondition(BaseModel):
    """Store condition and consequence of an item inspection."""

    divisor: int
    true: int
    false: int


class Monkey(BaseModel):
    """A monkey."""

    items: list[int]
    raw_operation: str
    test: ItemCondition
    inspections: int = 0
    worry_divisor: int = 3

    def parse_worry(self, current: int, divisor: int | None):
        """Parse worry instructions."""
        divisor = divisor or self.test.divisor
        _, __, left, operator_key, right = self.raw_operation.replace(
            "old", str(current)
        ).split(" ")

        return (
            OPERATORS[operator_key](int(left), int(right)) // self.worry_divisor % divisor
        )

    def do_business(self, divisor: int | None) -> tuple[int, int]:
        """Conduct monkey business."""
        self.inspections += 1
        worry_level = self.parse_worry(self.items.pop(0), divisor)

        return (
            self.test.true if worry_level % self.test.divisor == 0 else self.test.false,
            worry_level,
        )


class StealingAnimals(BaseModel):
    """A number of stealing animals."""

    monkeys: list[Monkey]

    @property
    def common_divisor(self) -> int:
        """Find common divisor."""
        return reduce(lambda x, y: x * y, [d.test.divisor for d in self.monkeys])

    def run_round(self) -> None:
        """Run a single round."""
        for monkey in self.monkeys:
            while monkey.items:
                to_monkey, worry = monkey.do_business(divisor=self.common_divisor)
                self.monkeys[to_monkey].items.append(worry)

    def result_string(self) -> str:
        """Determine string to show result."""
        results: list[str] = []
        for index, monkey in enumerate(self.monkeys):
            results.append(
                f"Monkey {index} inspected items {monkey.inspections} "
                f"times and is holding: {monkey.items}"
            )
        return "\n".join(results)

    def most_active(self) -> int:
        """Find most active monkeys."""
        monkeys = sorted(self.monkeys, key=lambda x: x.inspections, reverse=True)
        return monkeys[0].inspections * monkeys[1].inspections


def _parse_monkey(block: str, worry_divisor: int = 3) -> Monkey:
    """Parse text into Monkey object."""
    configuration: dict[str, str] = {}

    for line in block.splitlines():
        key, value = line.strip().split(":")
        configuration[key] = value.strip()

    return Monkey(
        items=configuration["Starting items"].split(", "),
        raw_operation=configuration["Operation"],
        test=ItemCondition(
            divisor=configuration["Test"].split(" ")[-1],
            true=configuration["If true"].split(" ")[-1],
            false=configuration["If false"].split(" ")[-1],
        ),
        worry_divisor=worry_divisor,
    )


@click.command(name="day11")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 10."""
    animals = StealingAnimals(
        monkeys=[_parse_monkey(l) for l in path.read_text().split("\n\n") if l]
    )
    for _ in range(20):
        animals.run_round()
    print(animals.result_string())
    print(f"[1] Most active product: {animals.most_active()}")

    del animals

    animals = StealingAnimals(
        monkeys=[_parse_monkey(l, 1) for l in path.read_text().split("\n\n") if l]
    )
    for _ in range(10_000):
        animals.run_round()
    print(animals.result_string())
    print(f"[2] Most active product: {animals.most_active()}")
