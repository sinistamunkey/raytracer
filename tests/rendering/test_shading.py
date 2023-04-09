from unittest.mock import Mock, call

import pytest
from pytest_mock import MockerFixture

from raytracer.core.types.entities import Light, Material, Scene, Sphere
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour
from raytracer.rendering.shading import Shader


@pytest.fixture
def camera() -> Point:
    return Point(0, 0, -1)


@pytest.fixture
def light() -> Light:
    return Light(position=Point(x=1.5, y=-0.5, z=-10.0), colour=Colour(255, 255, 255))


@pytest.fixture
def material() -> Material:
    return Material(colour=Colour(255, 0, 0), ambient=0.05, diffuse=1.0, specular=1.0)


@pytest.fixture
def sphere(material: Material) -> Sphere:
    return Sphere(
        name="Sphere 1",
        centre=Point(0, 0, 0),
        material=material,
        radius=0.5,
    )


@pytest.fixture
def scene(camera: Point, sphere: Sphere, light: Light) -> Scene:
    return Scene(
        camera=camera,
        objects=[sphere],
        lights=[light],
        width=10,
        height=10,
    )


class TestShader:
    def test_shade(
        self,
        scene: Scene,
        sphere: Sphere,
        mocker: MockerFixture,
        light: Point,
        material: Material,
        camera: Point,
    ) -> None:
        """
        GIVEN a scene
        AND an object hit by a ray
        WHEN calling shade
        THEN run diffuse shading
        AND specular shading
        """
        # GIVEN
        shader = Shader()
        diffuse = Mock(return_value=Colour(1, 0, 0))
        specular = Mock(return_value=Colour(1, 3, 0))
        mocker.patch.object(shader, "_diffuse", diffuse)
        mocker.patch.object(shader, "_specular", specular)
        manager = Mock()
        manager.attach_mock(diffuse, "diffuse")
        manager.attach_mock(specular, "specular")
        expected = Colour(2, 3, 0)

        # WHEN
        actual = shader.shade(scene=scene, obj_hit=sphere, hit_pos=Point(0, 0, 1))
        assert actual == expected
        manager.assert_has_calls(
            [
                call.diffuse(
                    light=light,
                    material=material,
                    hit_pos=Point(0, 0, 1),
                    normal=sphere.normal(Point(0, 0, 1)),
                ),
                call.specular(
                    light=light,
                    material=material,
                    normal=sphere.normal(Point(0, 0, 1)),
                    hit_pos=Point(0, 0, 1),
                    to_cam=camera - Point(0, 0, 1),
                ),
            ]
        )

    def test_diffuse(self, light: Light, material: Material, sphere: Sphere) -> None:
        # GIVEN
        shader = Shader()
        hit_pos = Point(0.5, 0.5, -0.5)
        normal = sphere.normal(hit_pos)
        expected = Colour(145, 0, 0)

        # WHEN
        actual = shader._diffuse(
            light=light, material=material, hit_pos=hit_pos, normal=normal
        )

        # THEN
        assert actual == expected

    def test_specular(
        self, light: Light, material: Material, sphere: Sphere, camera: Point
    ) -> None:
        # GIVEN
        shader = Shader()
        hit_pos = Point(0, 0, -0.5)
        normal = sphere.normal(hit_pos)
        expected = Colour(188, 188, 188)

        # WHEN
        actual = shader._specular(
            light=light,
            material=material,
            hit_pos=hit_pos,
            normal=normal,
            to_cam=camera - hit_pos,
        )

        # THEN
        assert actual == expected
