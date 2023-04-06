import math
from dataclasses import dataclass
from typing import Self, Union


@dataclass
class BaseVector:
    x: float
    y: float
    z: float

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.dot_product(other=self))

    def dot_product(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self) -> Self:
        return self / self.magnitude

    def __add__(self, other: Self) -> Self:
        cls = self.__class__
        return cls(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        cls = self.__class__
        return cls(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __mul__(self, other: Union[float, int]) -> Self:
        cls = self.__class__
        return cls(x=self.x * other, y=self.y * other, z=self.z * other)

    def __rmul__(self, other: Union[float, int]) -> Self:
        return self.__mul__(other)

    def __truediv__(self, other: Union[float, int]) -> Self:
        cls = self.__class__
        return cls(
            x=self.x / other,
            y=self.y / other,
            z=self.z / other,
        )


@dataclass
class Vector(BaseVector):
    pass


@dataclass
class Point(BaseVector):
    """A defined point in a 3D space"""

    pass
