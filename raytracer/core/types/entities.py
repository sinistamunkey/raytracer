import math
from dataclasses import dataclass, field
from typing import Optional, Self, Sequence

from raytracer.core.types.base import Loadable
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

    @classmethod
    def from_object(cls, data: dict, width: int, height: int) -> "Scene":
        return Scene(
            camera=Point.from_object(data["camera"]),
            objects=[Sphere.from_object(obj_data) for obj_data in data["objects"]],
            lights=[Light.from_object(light_data) for light_data in data["lights"]],
            width=width,
            height=height,
        )


@dataclass
class Light(Loadable):
    position: Point
    colour: Colour

    @classmethod
    def from_object(cls, data: dict) -> "Light":
        return cls(
            position=Point.from_object(data["position"]),
            colour=Colour.from_hex(data["colour"]),
        )


@dataclass
class BaseMaterial(Loadable):
    ambient: float = 0.05
    diffuse: float = 1.0
    specular: float = 1.0
    reflection: float = 0.5

    def colour_at(self, position: Point) -> Colour:
        raise NotImplementedError  # pragma: nocover

    @classmethod
    def from_object(cls, data: dict) -> Self:
        raise NotImplementedError  # pragma: nocover


@dataclass
class Material(BaseMaterial):
    colour: Colour = field(default_factory=Colour)

    def colour_at(self, position: Point) -> Colour:
        return self.colour

    @classmethod
    def from_object(cls, data: dict) -> "Material":
        return cls(
            colour=Colour.from_hex(data["attributes"]["colour"]),
            ambient=data["attributes"]["ambient"],
            diffuse=data["attributes"]["diffuse"],
            specular=data["attributes"]["specular"],
            reflection=data["attributes"]["reflection"],
        )


@dataclass
class ChequeredMaterial(BaseMaterial):
    colour_1: Colour = field(default_factory=Colour)
    colour_2: Colour = field(default_factory=Colour)

    def colour_at(self, position: Point) -> Colour:
        size = 1.0  # smaller number is larger square
        delta = 5.0
        if int((position.x + delta) * size) % 2 == int(position.z * size) % 2:
            return self.colour_2
        return self.colour_1

    @classmethod
    def from_object(cls, data: dict) -> "ChequeredMaterial":
        return cls(
            ambient=data["attributes"]["ambient"],
            diffuse=data["attributes"]["diffuse"],
            specular=data["attributes"]["specular"],
            reflection=data["attributes"]["reflection"],
            colour_1=Colour.from_hex(data["attributes"]["colour_1"]),
            colour_2=Colour.from_hex(data["attributes"]["colour_2"]),
        )


@dataclass
class Primitive(Loadable):
    name: str
    centre: Point
    material: "BaseMaterial"

    def intersects(self, ray: "Ray") -> Optional[float]:
        raise NotImplementedError  # pragma: nocover

    def normal(self, surface_point: Point) -> Point:
        return (surface_point - self.centre).normalize()

    @classmethod
    def from_object(cls, data: dict) -> Self:
        raise NotImplementedError  # pragma: nocover


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

    @classmethod
    def from_object(cls, data: dict) -> "Sphere":
        import sys

        material_name = data["attributes"]["material"]["type"]
        try:
            material_cls = getattr(sys.modules[__name__], material_name)
        except AttributeError:
            raise ValueError(f"'{material_name}' could not be found")
        if not issubclass(material_cls, BaseMaterial):
            raise ValueError(f"'{material_name}' is not a valid material")
        return cls(
            name=data["attributes"]["name"],
            centre=Point.from_object(data["attributes"]["centre"]),
            radius=data["attributes"]["radius"],
            material=material_cls.from_object(data["attributes"]["material"]),
        )
