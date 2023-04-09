import click

from raytracer.rendering.cli.render_scene import render_scene

cli = click.Group("rendering", commands=[render_scene])
