import os
from uuid import uuid4

import click

from raytracer.core import config
from raytracer.core.types.entities import Scene, Sphere
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour
from raytracer.imaging.service import ImageService
from raytracer.rendering.engine import RenderEngine


@click.command
def ball(width: int = 320, height: int = 200) -> None:
    """
    Generates a ball image to the filesystem

    :param width: The width (in pixels) of the image.
    :param height: The height (in pixes) of the image.
    """
    image_service = ImageService()
    camera = Point(x=0, y=0, z=-1)
    objects = [
        Sphere(
            centre=Point(x=0, y=0, z=0), radius=0.5, material=Colour.from_hex("#FF0000")
        )
    ]
    scene = Scene(camera=camera, objects=objects, width=width, height=height)
    engine = RenderEngine()
    image = engine.render(scene=scene)

    filepath = os.path.join(config.OUT_DIR, f"{uuid4()}.ppm")
    with open(filepath, "w") as image_file:
        image_service.render(canvas=image, image_file=image_file)
    click.echo(f"Generated file: {filepath}")


cli = click.Group(commands={"ball": ball})
