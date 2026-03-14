from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def menu(title, options):
    """Render a nice menu using Rich."""
    table = Table(show_header=False, box=box.SIMPLE_HEAVY, expand=True)
    for key, label in options.items():
        table.add_row(f"[bold cyan]{key}[/]", str(label))

    console.print(
        Panel(
            table,
            title=f"[bold yellow]{title}[/]",
            border_style="bright_blue",
            padding=(1, 2),
        )
    )


def print_table(headers, rows, title=None):
    """Render a table with Rich."""
    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
        expand=True,
    )
    for h in headers:
        table.add_column(str(h))

    for row in rows:
        table.add_row(*(str(col) for col in row))

    renderable = (
        Panel(
            table,
            title=f"[bold green]{title}[/]" if title else None,
            border_style="bright_blue",
            padding=(1, 2),
        )
        if title
        else table
    )
    console.print(renderable)


def success(msg: str):
    console.print(f"[bold green]✅ {msg}[/]")


def error(msg: str):
    console.print(f"[bold red]❌ {msg}[/]")


def info(msg: str):
    console.print(f"[bold cyan]{msg}[/]")