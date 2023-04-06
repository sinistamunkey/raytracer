import os
from random import randint
from uuid import uuid4

import click

from raytracer.core import config
from raytracer.imaging.constants import MAX_COLOUR
from raytracer.imaging.service import ImageService
from raytracer.imaging.types import Canvas, Pixel


@click.command
def random_image(width: int = 640, height: int = 480) -> None:
    """
    Generates a random image to the filesystem

    :param width: The width (in pixels) of the image.
    :param height: The height (in pixes) of the image.
    :returns: The full filepath of the random image.
    """
    image_service = ImageService()
    canvas = Canvas(width=width, height=height)
    progress = 0
    total_pixels = width * height
    with click.progressbar(length=total_pixels, label="Generating image") as bar:
        for y in range(height):
            for x in range(width):
                canvas.paint(
                    x=x,
                    y=y,
                    pixel=Pixel(
                        r=randint(0, MAX_COLOUR),
                        g=randint(0, MAX_COLOUR),
                        b=randint(0, MAX_COLOUR),
                    ),
                )
                progress += 1
                bar.update(progress)
    filepath = os.path.join(config.OUT_DIR, f"{uuid4()}.ppm")
    with open(filepath, "w") as image_file:
        image_service.render(canvas=canvas, image_file=image_file)
    click.echo(f"Generated file: {filepath}")


cli = click.Group(commands={"random-image": random_image})
