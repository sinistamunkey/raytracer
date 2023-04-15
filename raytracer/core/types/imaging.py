import enum
from dataclasses import dataclass

from raytracer.core.constants import MIN_COLOUR
from raytracer.core.types.colour import Colour  # type: ignore


class ImageFormat(enum.Enum):
    BMP = ".bmp"
    JPEG = ".jpeg"
    PNG = ".png"
    PPM = ".ppm"


@dataclass
class Canvas:
    width: int
    height: int

    @property
    def pixels(self) -> list[list[Colour]]:
        return self._pixels

    def __post_init__(self) -> None:
        # Create canvas for the pixels based on the given width and height
        self._pixels: list[list[Colour]] = [
            [DEFAULT_PIXEL for _ in range(self.width)] for _ in range(self.height)
        ]

    def paint(self, x: int, y: int, pixel: Colour) -> None:
        self._pixels[y][x] = pixel

    def set_row(self, index: int, row: list[Colour]) -> None:
        self._pixels[index] = row


DEFAULT_PIXEL = Colour(r=MIN_COLOUR, g=MIN_COLOUR, b=MIN_COLOUR)
