import click

from raytracer.imaging.cli import cli as imaging_cli

cli = click.Group(commands={"imaging": imaging_cli})

if __name__ == "__main__":
    cli()
