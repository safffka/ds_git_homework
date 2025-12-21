"""Console script for ds_git_homework."""

import typer
from rich.console import Console
from typing import Any
from ds_git_homework import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> Any:
    """Console script for ds_git_homework."""
    console.print("Replace this message by putting your code into "
                  "ds_git_homework.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
