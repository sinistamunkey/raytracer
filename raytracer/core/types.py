import math
from typing import Union

import pydantic


class Vector(pydantic.BaseModel):
    x: float
    y: float
    z: float

    @property
    def magnitude(self) -> float:
        value = self.dot_product(other=self)
        return math.sqrt(value)

    def dot_product(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self, other: "Vector") -> "Vector":
        return self / other.magnitude

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __mul__(self, other: Union[float, int]) -> "Vector":
        assert not isinstance(
            other, Vector
        ), "Cannot multiply a vector by another vector"
        return Vector(x=self.x * other, y=self.y * other, z=self.z * other)

    def __rmul__(self, other: Union[float, int]) -> "Vector":
        return self.__mul__(other)

    def __truediv__(self, other: Union[float, int]) -> "Vector":
        assert not isinstance(other, Vector), "Cannot divide a vector by another vector"
        return Vector(
            x=self.x / other,
            y=self.y / other,
            z=self.z / other,
        )
