import os
import shutil
import tempfile
from typing import Callable, Optional, TextIO

from PIL import Image

from raytracer.core.constants import MAX_COLOUR
from raytracer.core.types.imaging import Canvas, ImageFormat


class ImageService:
    def save(
        self,
        canvas: Canvas,
        filepath: str,
        update_func: Optional[Callable[[int], None]] = None,
    ) -> str:
        _, extension = os.path.splitext(filepath.lower())
        image_format = ImageFormat(extension)
        with tempfile.NamedTemporaryFile(
            suffix=ImageFormat.PPM.value, delete=False
        ) as tmp_img:
            tmp_img.close()
            with open(tmp_img.name, "w") as image_file:
                self._render(
                    canvas=canvas, image_file=image_file, update_func=update_func
                )

            if image_format == ImageFormat.PPM:
                shutil.copy(tmp_img.name, filepath)
                return filepath
            Image.open(tmp_img.name).save(filepath)
            return filepath

    def _render(
        self,
        canvas: Canvas,
        image_file: TextIO,
        update_func: Optional[Callable[[int], None]] = None,
    ) -> None:
        image_file.write(self._generate_header(canvas))
        for row in canvas.pixels:
            line = " ".join([f"{pixel.r} {pixel.g}  {pixel.b}" for pixel in row])
            image_file.write(f"{line}\n")
            if update_func:
                update_func(1)

    def _generate_header(self, canvas: Canvas) -> str:
        return f"P3 {canvas.width} {canvas.height}\n{MAX_COLOUR}\n"
