"""Main CLI entry point."""

import typer
from importlib import metadata

APP_NAME = 'xit'

cli_app = typer.Typer(
    help="""Tools to boost your productivity.""",
    no_args_is_help=True,
)


@cli_app.command(help=f"Display {APP_NAME}'s version.")
def version(raw: bool = False):
    """Display version information."""
    res = metadata.version(APP_NAME)
    if not raw:
        res = f'{APP_NAME} {res}'
    typer.echo(res)


@cli_app.command(hidden=True, deprecated=True)
def hello(message: str = f"Hello {APP_NAME}"):
    """Display a message."""
    typer.echo(message)
