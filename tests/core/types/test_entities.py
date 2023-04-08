from typing import Optional

import pytest

from raytracer.core.types.entities import Material, Primitive, Ray, Sphere
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour


class Sidebar(Primitive):
    def intersects(self, ray: "Ray") -> Optional[float]:
        return None


class TestPrimitive:
    def test_normal(self) -> None:
        pass


class TestSphere:
    @pytest.mark.parametrize(
        "ray,sphere,expected",
        [
            pytest.param(
                Ray(origin=Point(0, 0, -1), direction=Point(0, 0, 6)),
                Sphere(
                    centre=Point(0, 0, 0),
                    material=Material(colour=Colour(255, 0, 0)),
                    radius=0.5,
                ),
                0.5,
                id="Ray intersects with sphere",
            ),
            pytest.param(
                Ray(origin=Point(20, 20, -1), direction=Point(20, 20, 6)),
                Sphere(
                    centre=Point(0, 0, 0),
                    material=Material(colour=Colour(255, 0, 0)),
                    radius=0.5,
                ),
                None,
                id="Ray does not intersect with sphere",
            ),
        ],
    )
    def test_intersects(
        self, ray: Ray, sphere: Sphere, expected: Optional[float]
    ) -> None:
        actual = sphere.intersects(ray=ray)
        assert actual == expected

    def test_normal(self) -> None:
        shape = Sidebar(
            centre=Point(0, 0, 0),
            material=Material(colour=Colour(), ambient=0.0, diffuse=0.0, specular=0.0),
        )
        actual = shape.normal(Point(1, 2, 3))
        expected = Point(0.2672612419124244, 0.5345224838248488, 0.8017837257372732)
        assert actual == expected


class TestRay:
    def test_direction_normalized(self) -> None:
        ray = Ray(origin=Point(0, 0, 0), direction=Point(1.123, 2.456, 6))
        actual = ray.direction
        expected = Point(0.17067526645373582, 0.37326665575278284, 0.9118892241517497)
        assert actual == expected
