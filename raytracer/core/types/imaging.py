from dataclasses import dataclass
from typing import Any, Union

from raytracer.core.constants import MAX_COLOUR, MIN_COLOUR


@dataclass
class Pixel:
    r: int = 0
    g: int = 0
    b: int = 0

    def __add__(self, other: "Pixel") -> "Pixel":
        return Pixel(
            r=self.r + other.r,
            g=self.g + other.g,
            b=self.b + other.b,
        )

    def __sub__(self, other: "Pixel") -> "Pixel":
        return Pixel(
            r=self.r - other.r,
            g=self.g - other.g,
            b=self.b - other.b,
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ["r", "g", "b"]:
            # Clamp the value to the min and maxes and ensure it's a full number
            value = round(max(min(value, MAX_COLOUR), MIN_COLOUR))
        super().__setattr__(name, value)

    def __mul__(self, other: Union[float, int]) -> "Pixel":
        return Pixel(
            r=int(self.r * other), g=int(self.g * other), b=int(self.b * other)
        )

    def __rmul__(self, other: Union[float, int]) -> "Pixel":
        return self.__mul__(other)

    def __truediv__(self, other: Union[float, int]) -> "Pixel":
        return Pixel(
            r=int(self.r / other),
            g=int(self.g / other),
            b=int(self.b / other),
        )

    @classmethod
    def from_hex(cls, value: str) -> "Pixel":
        red = int(value[1:3], 16)
        green = int(value[3:5], 16)
        blue = int(value[5:7], 16)
        return cls(r=red, g=green, b=blue)


@dataclass
class Canvas:
    width: int
    height: int

    @property
    def pixels(self) -> list[list[Pixel]]:
        return self._pixels

    def __post_init__(self) -> None:
        # Create canvas for the pixels based on the given width and height
        self._pixels: list[list[Pixel]] = [
            [DEFAULT_PIXEL for _ in range(self.width)] for _ in range(self.height)
        ]

    def paint(self, x: int, y: int, pixel: Pixel) -> None:
        self._pixels[y][x] = pixel


DEFAULT_PIXEL = Pixel(r=MIN_COLOUR, g=MIN_COLOUR, b=MIN_COLOUR)
