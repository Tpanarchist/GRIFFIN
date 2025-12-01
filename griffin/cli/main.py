from __future__ import annotations

from typing import Tuple

import logging

import typer
from rich.console import Console

from griffin.ace.ace_message import ACEMessage
from griffin.ace.stack import ACEStack
from griffin.core.version import __version__, get_version
from griffin.infra.config import get_config, setup_logging

app = typer.Typer(add_completion=False, help="G.R.I.F.F.I.N. command-line interface")
console = Console()

def main(argv: Tuple[str, ...] = ()) -> int:
    """Simple programmatic entry used by tests."""
    cfg = get_config()
    ver = get_version()
    banner = f"G.R.I.F.F.I.N. v{ver} — {cfg.env}"
    print(banner)
    return 0

@app.callback()
def main_callback(
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Increase log verbosity (-v=INFO, -vv=DEBUG).",
    ),
) -> None:
    cfg = get_config()

    if verbose >= 2:
        level = "DEBUG"
    elif verbose == 1:
        level = "INFO"
    else:
        level = cfg.log_level

    setup_logging(level)
    logging.getLogger(__name__).debug("CLI initialized with config %s", cfg.model_dump())

@app.command()
def ping() -> None:
    """Sanity check: create a message, send into ACEStack and echo reply."""
    stack = ACEStack()
    msg = ACEMessage(content="ping from CLI", source="cli", role="user")
    console.print(f"[bold cyan]G.R.I.F.F.I.N.[/bold cyan] v{__version__}")
    console.print("Message envelope:")
    console.print(msg.to_dict())

    reply = stack.send(msg)
    console.print("[bold green]Reply from ACEStack:[/bold green]")
    console.print(reply.to_dict())

def run() -> None:
    app()

if __name__ == "__main__":
    run()
