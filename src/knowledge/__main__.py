"""Name the commands and hand each one the arguments it was given.

The work lives elsewhere; this module decides only what was asked for. Keeping the two apart is what lets
a command be tested by calling it, rather than by driving a process and reading what it printed.
"""


def main() -> None:
    """Run the command named on the command line."""
