"""Solution for day 6 of Advent of Code."""
# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods
from __future__ import annotations

from enum import Enum
from pathlib import Path

import click
import click_pathlib
from pydantic import BaseModel

MAX_SIZE = 100000


class CommandType(Enum):
    """Available command types."""

    CD: str = "cd"
    LS: str = "ls"


class Command(BaseModel):
    """A command on the filesystem."""

    name: CommandType
    argument: str | None = None
    output_data: list[str] | None = None

    @property
    def outputs(self) -> tuple[dict[str, Directory], list[File]] | None:
        """Convert output_data into a tuple of directories and files."""
        if not self.output_data:
            return self.output_data

        directories, files = {}, []

        for line in list(self.output_data):
            kind, name = line.split(" ")

            if kind == "dir":
                directories[name] = Directory(name=name)
            else:
                files.append(File(name=name, size=int(kind)))

        return directories, files

    def __str__(self) -> str:
        return f"Command(name={self.name}, argument={self.argument}, outputs={self.outputs})"


class File(BaseModel):
    """A single file."""

    name: str
    size: int


class Directory(BaseModel):
    """Represents a directory."""

    name: str
    directories: dict[str, Directory] = {}
    files: list[File] = []

    @property
    def size(self) -> int:
        """Determine size of directory."""
        return sum(
            [f.size for f in self.files] + [d.size for _, d in self.directories.items()]
        )

    def execute_commands(self, commands: list[Command]) -> Directory:
        """Execute commands within the directory."""
        command = commands.pop(0)

        match command:
            case Command(name=CommandType.CD):
                if command.argument == "..":
                    return self
                self.directories[command.argument].execute_commands(commands)
            case Command(name=CommandType.LS):
                self.directories, self.files = command.outputs

        if commands:
            return self.execute_commands(commands)
        return self

    @property
    def maxed_size(self) -> int:
        """Determine the total size of a directory, and only let them count
        if it's smaller than MAX_SIZE."""
        total_size = 0
        size_increment = self.size

        if size_increment < MAX_SIZE:
            total_size += size_increment
        # pylint: disable=consider-using-generator
        total_size += sum(
            [self.directories[sub_folder].maxed_size for sub_folder in self.directories]
        )

        return total_size

    def efficient_delete(
        self, delete_size: int, found_directory: Directory | None = None
    ) -> Directory | None:
        """Determine which directory to delete given a certain required amount of free space."""
        if (
            found_directory and delete_size <= self.size < found_directory.size
        ) or delete_size <= self.size:
            found_directory = self

        for directory in self.directories:
            found_directory = self.directories[directory].efficient_delete(
                delete_size, found_directory
            )

        return found_directory


def _parse_into_command(data: list[str]) -> Command:
    """Parse a block of data into a Command object."""
    command_arguments = data[0].split(" ")
    base_command = Command(
        name=getattr(CommandType, command_arguments[0].upper()),
        argument=command_arguments[1] if len(command_arguments) > 1 else None,
    )
    if len(data) > 1:
        setattr(base_command, "output_data", data[1:])
    return base_command


@click.command(name="day07")
@click.option("--path", type=click_pathlib.Path(exists=True))
def main(path: Path) -> None:
    """Solve day 7."""
    command_blocks = path.read_text().split("$ ")
    commands: list[Command] = []

    for block in command_blocks:
        if block := block.strip():
            commands.append(_parse_into_command(block.split("\n")))

    directories: dict[str, Directory] = {
        "/": Directory(name=commands[0].argument).execute_commands(commands[1:])
    }

    print(f"[1] Total size: {directories['/'].maxed_size}")

    total_disk_space = 70000000
    required_space = 30000000
    required_delete = required_space - (total_disk_space - directories["/"].size)

    print(f"[x] Required to delete: {required_delete}")
    delete_directory = directories["/"].efficient_delete(required_delete)
    print(
        f"[2] Delete directory: {delete_directory.name}. Its size is "
        f"{delete_directory.size}, which leaves a free space "
        f"of {delete_directory.size - required_delete}"
    )
