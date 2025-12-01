from __future__ import annotations

from typing import Tuple

import logging

import typer
from rich.console import Console

from griffin.ace.ace_message import ACEMessage
from griffin.ace.stack import ACEStack
from griffin.core.version import __version__, get_version
from griffin.infra.config import get_config, setup_logging

# NEW imports:
from griffin.infra.http_client import HTTPXHTTPPort
from griffin.services.esi_characters import ESICharactersService
from rich.table import Table

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

@app.command()
def whois(character_id: int = typer.Argument(..., help="EVE character ID")) -> None:
    """Look up basic public info for a character via ESI."""
    cfg = get_config()
    logging.getLogger(__name__).info(
        "whois lookup for character_id=%s using ESI base %s", character_id, cfg.esi_base_url
    )

    with HTTPXHTTPPort() as http:
        service = ESICharactersService(http=http)
        char = service.get_public_character(character_id)

    table = Table(title=f"Character {char.name} ({char.character_id})")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Name", char.name)
    table.add_row("Character ID", str(char.character_id))
    table.add_row("Corporation ID", str(char.corporation_id or "—"))
    table.add_row("Alliance ID", str(char.alliance_id or "—"))
    table.add_row("Security Status", f"{char.security_status:.2f}" if char.security_status is not None else "—")
    table.add_row("Birthday", char.birthday.isoformat() if char.birthday else "—")
    table.add_row("Race ID", str(char.race_id or "—"))

    console.print(f"[bold cyan]G.R.I.F.F.I.N.[/bold cyan] v{__version__}")
    console.print(table)

@app.command()
def ace(query: str = typer.Argument(..., help="Send a query to the ACE stack")) -> None:
    """Talk to the ACE stack. Use 'ace:' prefix to invoke the Aspirational layer."""
    stack = ACEStack.from_config()
    msg = ACEMessage(source="cli", role="user", content=query)
    reply = stack.send(msg)

    console.print(f"[bold cyan]ACE Reply[/bold cyan]:")
    console.print(reply.content)

def run() -> None:
    app()

if __name__ == "__main__":
    run()
