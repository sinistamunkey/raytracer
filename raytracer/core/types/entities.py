import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence

from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour
from raytracer.rendering.constants import SCENE_ABSOLUTE_BOTTOM, SCENE_ABSOLUTE_TOP


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
    lights: Sequence["Light"]
    width: int
    height: int

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    def get_aspect_boundries(self) -> tuple[float, float]:
        """
        Returns the real boundaries of the scene based on the aspect ratio.
        """
        return (
            SCENE_ABSOLUTE_TOP / self.aspect_ratio,
            SCENE_ABSOLUTE_BOTTOM / self.aspect_ratio,
        )

    def get_horizontal_and_vertical_steps(self) -> tuple[float, float]:
        """
        Returns a tuple indicating the steps to iterate over due to
        the scene being not an exact square.
        """
        scene_top, scene_bottom = self.get_aspect_boundries()
        return (
            (SCENE_ABSOLUTE_BOTTOM - SCENE_ABSOLUTE_TOP) / (self.width - 1),
            (scene_bottom - scene_top) / (self.height - 1),
        )


@dataclass
class Light:
    position: Point
    colour: Colour


@dataclass
class Material:
    colour: Colour
    ambient: float = 0.0
    diffuse: float = 0.0
    specular: float = 0.0

    def colour_at(self, position: Point) -> Colour:
        return self.colour


@dataclass
class Primitive(ABC):
    centre: Point
    material: "Material"

    @abstractmethod
    def intersects(self, ray: "Ray") -> Optional[float]:
        pass  # pragma: nocover

    def normal(self, surface_point: Point) -> Point:
        return (surface_point - self.centre).normalize()


@dataclass
class Sphere(Primitive):
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
