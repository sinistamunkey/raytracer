import click

from raytracer.imaging.cli.ball import render_ball

cli = click.Group(commands={"ball": render_ball})
