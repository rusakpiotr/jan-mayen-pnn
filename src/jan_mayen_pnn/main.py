import click


@click.group()
def cli() -> None:
    """Jan Mayen PNN command line interface."""


@cli.command()
@click.option("--name", default="Jan Mayen", help="Who to greet.")
def hello(name: str) -> None:
    """Print a greeting."""
    click.echo(f"Hello from {name}!")

@cli.command()
def run_example() -> str:
    pass

if __name__ == "__main__":
    cli()
