import json
import os
from typing import Optional
from uuid import uuid4

import click

from raytracer.core import config
from raytracer.core.types.entities import Scene
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
@click.option(
    "-s",
    "--scene",
    "scene_name",
    default="scene_1",
    required=False,
    type=str,
    help="The name of a scene in the scenes directory (excluding extension) to use.",
)
def render_scene(
    width: int = 320,
    height: int = 200,
    scene_name: str = "scene_1",
    filename: Optional[str] = None,
) -> None:
    scene = _load_scene_from_file(scene_name=scene_name, width=width, height=height)
    engine = RenderEngine(shader=Shader())
    with click.progressbar(length=width * height, label="Rendering scene") as bar:
        canvas = engine.render(scene=scene, update_func=bar.update)

    filename = filename or f"{uuid4()}.ppm"
    filepath = os.path.join(config.OUT_DIR, filename)
    with click.progressbar(length=height, label="Saving file") as bar:
        saved_file = ImageService().save(
            canvas=canvas, filepath=filepath, update_func=bar.update
        )
    click.echo(f"Generated files: {saved_file}")


def _load_scene_from_file(scene_name: str, width: int, height: int) -> Scene:
    scene_file = os.path.join(config.SCENE_DIR, f"{scene_name}.json")

    with open(scene_file, "r") as f:
        data = json.load(f)

    return Scene.from_object(data=data, width=width, height=height)
