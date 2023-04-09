import logging

import click

from raytracer.rendering.cli import cli as rendering_cli

logging.basicConfig(
    filename="output.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

cli = click.Group(commands=[rendering_cli])

if __name__ == "__main__":
    cli()
