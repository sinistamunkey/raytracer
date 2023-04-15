from typing import Optional
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from raytracer.core.types.entities import Light, Material, Primitive, Ray, Scene, Sphere
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour
from raytracer.rendering.engine import RenderEngine
from raytracer.rendering.shading import Shader


class FakeShader(Shader):
    def shade(self, *args, **kwargs):
        return Colour(255, 255, 255)


@pytest.fixture
def shader() -> FakeShader:
    return FakeShader()


@pytest.fixture
def scene() -> Scene:
    return Scene(
        width=2,
        height=2,
        camera=Point(0, 0, -1),
        objects=[
            Sphere(
                name="Sphere 1",
                centre=Point(0, 0, 0),
                material=Material(colour=Colour(0, 0, 0)),
                radius=0.5,
            )
        ],
        lights=[Light(position=Point(0, 0, 0), colour=Colour(0, 0, 0))],
    )


class TestRenderEngine:
    @pytest.fixture
    def engine(self, shader: FakeShader) -> RenderEngine:
        return RenderEngine(shader=shader)

    def test_render(
        self, scene: Scene, engine: RenderEngine, mocker: MockerFixture
    ) -> None:
        """
        GIVEN a scene
        WHEN calling render
        THEN yield an iterable containing indexes and row
        """
        # GIVEN
        expected = [
            (0, [Colour(0, 0, 0), Colour(0, 0, 0)]),
            (1, [Colour(0, 0, 0), Colour(0, 0, 0)]),
        ]

        # WHEN
        actual = list(engine.render(scene=scene))

        # THEN
        assert actual == expected

    def test_render_row(self, scene: Scene, engine: RenderEngine) -> None:
        """
        GIVEN a scene
        AND has a row of 2 columns
        WHEN calling render row with the first row
        THEN return a tuple of 0 and 10 colours
        """
        # GIVEN
        expected = (0, [Colour(0, 0, 0), Colour(255, 255, 255)])
        params = (
            scene,
            0,
            0,
            1,
            1,
        )

        # WHEN
        actual = engine._render_row(params)

        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        "find_nearest,expected",
        [
            pytest.param(
                Mock(
                    side_effect=[
                        (
                            1.0,
                            Sphere(
                                name="Sphere 1",
                                centre=Point(0, 0, 0),
                                material=Material(colour=Colour(0, 0, 0)),
                                radius=0.5,
                            ),
                        ),
                        (None, None),
                    ],
                ),
                Colour(255, 255, 255),
                id="Ray hits an object",
            ),
            pytest.param(
                Mock(return_value=(None, None)),
                Colour(0, 0, 0),
                id="Ray misses an object",
            ),
        ],
    )
    def test_render_pixel(
        self,
        scene: Scene,
        engine: RenderEngine,
        mocker: MockerFixture,
        find_nearest: Mock,
        expected: Colour,
    ) -> None:
        """
        GIVEN a scene
        AND a ray
        WHEN calling _render_pixel
        THEN colour the pixel if the ray intersects with an object
        """
        # GIVEN
        mocker.patch.object(engine, "_find_nearest", find_nearest)

        # WHEN
        actual = engine._render_pixel(
            ray=Ray(origin=Point(0, 0, 0), direction=Point(1, 1, 1)), scene=scene
        )

        # THEN
        assert actual == expected

    @pytest.mark.parametrize(
        "ray,expected_distance,expected_object",
        [
            pytest.param(
                Ray(origin=Point(0, 0, -1), direction=Point(0, 0, 1)),
                0.5,
                Sphere(
                    name="Sphere 1",
                    centre=Point(0, 0, 0),
                    material=Material(
                        colour=Colour(0, 0, 0),
                        ambient=0.05,
                        diffuse=1.0,
                        specular=1.0,
                        reflection=0.5,
                    ),
                    radius=0.5,
                ),
                id="Hits object",
            ),
            pytest.param(
                Ray(origin=Point(0, 0, 1), direction=Point(0, 0, 1)),
                None,
                None,
                id="Misses object",
            ),
        ],
    )
    def test_find_nearest(
        self,
        scene: Scene,
        engine: RenderEngine,
        ray: Ray,
        expected_distance: Optional[float],
        expected_object: Optional[Primitive],
    ) -> None:
        # WHEN
        actual_distance, actual_object = engine._find_nearest(scene=scene, ray=ray)

        # THEN
        assert actual_distance == expected_distance
        assert actual_object == expected_object
