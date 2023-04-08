import os
from typing import Optional
from uuid import uuid4

import click

from raytracer.core import config
from raytracer.core.types.entities import Light, Material, Scene, Sphere
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour
from raytracer.imaging.service import ImageService
from raytracer.rendering.engine import RenderEngine
from raytracer.rendering.shading import Shader


@click.command
@click.option(
    "-w",
    "--width",
    required=False,
    type=int,
    default=320,
    help="The height (in pixes) of the image.",
)
@click.option(
    "-h",
    "--height",
    required=False,
    type=int,
    default=200,
    help="The height (in pixels) of the image.",
)
@click.option(
    "-f",
    "--filename",
    required=False,
    type=str,
    help="The name of the file to create in the out directory.",
)
def render_ball(
    width: int = 320, height: int = 200, filename: Optional[str] = None
) -> None:
    image_service = ImageService()
    camera = Point(x=0, y=0, z=-1)
    objects = [
        Sphere(
            centre=Point(x=0, y=0, z=0),
            radius=0.5,
            material=Material(
                colour=Colour.from_hex("#FF0000"),
                ambient=0.05,
                diffuse=1.0,
                specular=1.0,
            ),
        )
    ]
    lights = [
        Light(
            position=Point(x=1.5, y=-0.5, z=-10.0), colour=Colour(r=255, g=255, b=255)
        )
    ]
    scene = Scene(
        camera=camera, objects=objects, lights=lights, width=width, height=height
    )
    engine = RenderEngine(shader=Shader())
    image = engine.render(scene=scene)

    if filename is not None:
        filepath = os.path.join(config.OUT_DIR, filename)
    else:
        filepath = os.path.join(config.OUT_DIR, f"{uuid4()}.ppm")
    with open(filepath, "w") as image_file:
        image_service.render(canvas=image, image_file=image_file)
    click.echo(f"Generated file: {filepath}")
