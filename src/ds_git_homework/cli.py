"""Console script for ds_git_homework."""

import typer
from rich.console import Console

from ds_git_homework.utils import do_something_useful

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for ds_git_homework."""
    console.print(
        "Replace this message by putting your code into "
        "ds_git_homework.cli.main"
    )
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    do_something_useful()


if __name__ == "__main__":
    app()
