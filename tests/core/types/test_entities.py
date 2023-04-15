from typing import Optional

import pytest

from raytracer.core.types.entities import (
    ChequeredMaterial,
    Light,
    Material,
    Primitive,
    Ray,
    Scene,
    Sphere,
)
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
                    name="Sphere 1",
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
                    name="Sphere 2",
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
            name="Sidebar! Sidebar!",
            centre=Point(0, 0, 0),
            material=Material(
                colour=Colour(0, 0, 0), ambient=0.0, diffuse=0.0, specular=0.0
            ),
        )
        actual = shape.normal(Point(1, 2, 3))
        expected = Point(0.2672612419124244, 0.5345224838248488, 0.8017837257372732)
        assert actual == expected

    def test_from_object(self) -> None:
        data = {
            "attributes": {
                "name": "Blue ball",
                "centre": {"x": 0.75, "y": -0.1, "z": 1},
                "radius": 0.6,
                "material": {
                    "type": "Material",
                    "attributes": {
                        "colour": "#0000FF",
                        "ambient": 0.05,
                        "diffuse": 1.0,
                        "specular": 1.0,
                        "reflection": 0.6,
                    },
                },
            }
        }
        expected = Sphere(
            name="Blue ball",
            centre=Point(x=0.75, y=-0.1, z=1),
            radius=0.6,
            material=Material(
                colour=Colour(r=0, g=0, b=255),
                ambient=0.05,
                diffuse=1.0,
                specular=1.0,
                reflection=0.6,
            ),
        )
        actual = Sphere.from_object(data=data)
        assert actual == expected

    def test_from_object_unknown_material(self) -> None:
        data = {
            "attributes": {
                "name": "Blue ball",
                "centre": {"x": 0.75, "y": -0.1, "z": 1},
                "radius": 0.6,
                "material": {
                    "type": "WTF",
                    "attributes": {
                        "colour": "#0000FF",
                        "ambient": 0.05,
                        "diffuse": 1.0,
                        "specular": 1.0,
                        "reflection": 0.6,
                    },
                },
            }
        }
        with pytest.raises(ValueError, match="'WTF' could not be found"):
            Sphere.from_object(data=data)

    def test_from_object_invalid_material(self) -> None:
        data = {
            "attributes": {
                "name": "Blue ball",
                "centre": {"x": 0.75, "y": -0.1, "z": 1},
                "radius": 0.6,
                "material": {
                    "type": "Sphere",
                    "attributes": {
                        "colour": "#0000FF",
                        "ambient": 0.05,
                        "diffuse": 1.0,
                        "specular": 1.0,
                        "reflection": 0.6,
                    },
                },
            }
        }
        with pytest.raises(ValueError, match="'Sphere' is not a valid material"):
            Sphere.from_object(data=data)


class TestRay:
    def test_direction_normalized(self) -> None:
        ray = Ray(origin=Point(0, 0, 0), direction=Point(1.123, 2.456, 6))
        actual = ray.direction
        expected = Point(0.17067526645373582, 0.37326665575278284, 0.9118892241517497)
        assert actual == expected


class TestMaterial:
    def test_from_object(self) -> None:
        data = {
            "attributes": {
                "colour": "#0000FF",
                "ambient": 0.05,
                "diffuse": 1.0,
                "specular": 1.0,
                "reflection": 0.6,
            }
        }
        actual = Material.from_object(data=data)
        expected = Material(
            colour=Colour(r=0, g=0, b=255),
            ambient=0.05,
            diffuse=1.0,
            specular=1.0,
            reflection=0.6,
        )
        assert actual == expected


class TestLight:
    def test_from_object(self) -> None:
        data = {"position": {"x": 1.5, "y": -0.5, "z": -10.0}, "colour": "#FFFFFF"}
        expected = Light(
            position=Point(x=1.5, y=-0.5, z=-10.0), colour=Colour(r=255, g=255, b=255)
        )
        actual = Light.from_object(data=data)
        assert actual == expected


class TestChequeredMaterial:
    def test_from_object(self) -> None:
        data = {
            "attributes": {
                "colour_1": "#420500",
                "colour_2": "#e6b87d",
                "ambient": 0.2,
                "diffuse": 1.0,
                "specular": 1.0,
                "reflection": 0.2,
            }
        }
        actual = ChequeredMaterial.from_object(data=data)
        expected = ChequeredMaterial(
            colour_1=Colour(r=66, g=5, b=0),
            colour_2=Colour(r=230, g=184, b=125),
            ambient=0.2,
            diffuse=1.0,
            specular=1.0,
            reflection=0.2,
        )
        assert actual == expected

    @pytest.mark.parametrize(
        "position,expected",
        [
            pytest.param(Point(2, 0, 2), Colour(r=0, g=0, b=0), id="Returns colour_1"),
            pytest.param(
                Point(3, 0, 2), Colour(r=255, g=255, b=255), id="Returns colour_2"
            ),
        ],
    )
    def test_colour_at(self, position: Point, expected: Colour) -> None:
        actual = ChequeredMaterial(
            colour_1=Colour(r=0, g=0, b=0), colour_2=Colour(r=255, g=255, b=255)
        ).colour_at(position=position)
        assert actual == expected


class TestScene:
    def test_from_object(self, scene_data: dict) -> None:
        expected = Scene(
            camera=Point(0, -0.35, -1),
            objects=[
                Sphere(
                    name="Blue ball",
                    centre=Point(x=0.75, y=-0.1, z=1),
                    radius=0.6,
                    material=Material(
                        colour=Colour(r=0, g=0, b=255),
                        ambient=0.05,
                        diffuse=1.0,
                        specular=1.0,
                        reflection=0.6,
                    ),
                )
            ],
            lights=[
                Light(
                    position=Point(x=1.5, y=-0.5, z=-10.0),
                    colour=Colour(r=255, g=255, b=255),
                )
            ],
            width=640,
            height=480,
        )
        actual = Scene.from_object(data=scene_data, width=640, height=480)
        assert actual == expected
