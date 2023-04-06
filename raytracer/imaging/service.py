from typing import TextIO

from raytracer.imaging.constants import MAX_COLOUR
from raytracer.imaging.types import Canvas


class ImageService:
    def render(self, canvas: Canvas, image_file: TextIO) -> None:
        image_file.write(self._generate_header(canvas))
        for row in canvas.pixels:
            line = " ".join([f"{pixel.r} {pixel.g}  {pixel.b}" for pixel in row])
            image_file.write(f"{line}\n")

    def _generate_header(self, canvas: Canvas) -> str:
        return f"P3 {canvas.width} {canvas.height}\n{MAX_COLOUR}\n"
