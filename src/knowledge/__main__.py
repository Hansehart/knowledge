"""Name the commands and hand each one the arguments it was given.

This module reads the command line and calls the matching command, which lives in a module of its own.
A test can then call a command's function with its arguments and check what it returns.
"""


def main() -> None:
    """Run the command named on the command line."""
