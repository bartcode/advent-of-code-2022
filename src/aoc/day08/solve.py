"""Solution for day 8 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

import logging
from pathlib import Path

import click
import click_pathlib
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def forrest_trees(trees: np.array, row: int, column: int) -> np.array:
    """Yield all combinations of rows and columns - in reversed order, too."""
    yield trees[row, column + 1 :]
    yield np.flip(trees[:row, column])

    yield trees[row + 1 :, column]
    yield np.flip(trees[row, :column])


def make_edges_visible(trees: np.array) -> np.array:
    """Set empty grid with all edges set to visible."""
    visible_trees = np.zeros_like(trees)
    visible_trees[0, :] = 1
    visible_trees[-1, :] = 1
    visible_trees[:, 0] = 1
    visible_trees[:, -1] = 1
    return visible_trees


def determine_visibility(tree_grid: np.array) -> np.array:
    """Determine visibility of each of the trees."""
    visible_trees = make_edges_visible(tree_grid)
    rows, columns = tree_grid.shape
    for row in range(1, rows - 1):
        for column in range(1, columns - 1):
            height = tree_grid[row, column]
            for line in forrest_trees(tree_grid, row, column):
                if np.all(line < height):
                    visible_trees[row, column] = 1
                    break
    return visible_trees


def viewing_distance(height: int, line: np.array) -> np.array:
    """Get viewing distance."""
    matches = np.where(line >= height)[0]
    return matches[0] + 1 if len(matches) else len(line)


def determine_tree_scores(tree_grid: np.array) -> np.array:
    """Determine scores of trees."""
    scores = np.zeros_like(tree_grid)
    rows, columns = tree_grid.shape
    for row in range(1, rows - 1):
        for column in range(1, columns - 1):
            height = tree_grid[row, column]
            distance = [
                viewing_distance(height, line)
                for line in forrest_trees(tree_grid, row, column)
            ]
            scores[row, column] = np.prod(distance)
    return scores


@click.command(name="day08")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 8."""
    trees = np.array(
        [
            [int(height) for height in tree_line]
            for tree_line in path.read_text().splitlines()
        ]
    )

    print(f"[1] Visible trees: {determine_visibility(trees).sum()}")
    print(f"[1] Tree scores: {determine_tree_scores(trees).max()}")
