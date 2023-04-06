import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence

from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Pixel


@dataclass
class Ray:
    """A one way line indicating a ray of light"""

    origin: Point
    direction: Point

    def __post_init__(self) -> None:
        self.direction = self.direction.normalize()


@dataclass
class Scene:
    camera: Point
    objects: Sequence["Primitive"]
    width: int
    height: int


@dataclass
class Primitive(ABC):
    material: "Pixel"

    @abstractmethod
    def intersects(self, ray: "Ray") -> Optional[float]:
        pass


@dataclass
class Sphere(Primitive):
    centre: Point
    radius: float

    def intersects(self, ray: "Ray") -> Optional[float]:
        sphere_to_ray = ray.origin - self.centre
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        discriminent = b * b - 4 * c

        if discriminent >= 0:
            distance: float = (-b - math.sqrt(discriminent)) / 2
            if distance > 0:
                return distance
        return None
