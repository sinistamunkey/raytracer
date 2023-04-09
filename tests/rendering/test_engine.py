from typing import Optional
from unittest.mock import Mock, call

import pytest
from pytest_mock import MockerFixture

from raytracer.core.types.entities import Light, Material, Primitive, Ray, Scene, Sphere
from raytracer.core.types.geometry import Point
from raytracer.core.types.imaging import Colour
from raytracer.rendering.engine import RenderEngine


@pytest.fixture
def shader() -> Mock:
    return Mock()


@pytest.fixture
def scene() -> Scene:
    return Scene(
        width=2,
        height=2,
        camera=Point(x=0, y=0, z=-1),
        objects=[
            Sphere(
                name="Sphere 1",
                centre=Point(0, 0, 0),
                material=Material(colour=Colour(0, 0, 0)),
                radius=0.5,
            )
        ],
        lights=[Light(position=Point(0, 0, 0), colour=Colour())],
    )


class TestRenderEngine:
    @pytest.fixture
    def engine(self, shader: Mock) -> RenderEngine:
        return RenderEngine(shader=shader)

    def test_render(
        self, scene: Scene, engine: RenderEngine, mocker: MockerFixture
    ) -> None:
        """
        GIVEN a scene
        WHEN calling render
        THEN fill the canvas with rendered pixels
        """
        # GIVEN
        render_pixel = Mock(return_value=Colour(r=255, g=255, b=255))
        mocker.patch.object(engine, "_render_pixel", render_pixel)
        expected = 3060  # If every pixel is white - this should be the colour total

        # WHEN
        canvas = engine.render(scene=scene)

        # THEN
        pixels = [pixel for row in canvas.pixels for pixel in row]
        actual = sum([pixel.r + pixel.g + pixel.b for pixel in pixels])
        assert actual == expected

    def test_render_updates_progress(
        self, scene: Scene, engine: RenderEngine, mocker: MockerFixture
    ) -> None:
        """
        GIVEN a scene
        WHEN calling render
        THEN fill the canvas with rendered pixels
        """
        # GIVEN
        update_func = Mock()
        render_pixel = Mock(return_value=Colour(r=255, g=255, b=255))
        mocker.patch.object(engine, "_render_pixel", render_pixel)

        # WHEN
        engine.render(scene=scene, update_func=update_func)

        # THEN
        assert update_func.mock_calls == [call(1), call(1), call(1), call(1)]

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
        shader: Mock,
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
        shader.shade.return_value = Colour(255, 255, 255)
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
                Ray(origin=Point(x=0, y=0, z=-1), direction=Point(0, 0, 1)),
                0.5,
                Sphere(
                    name="Sphere 1",
                    centre=Point(x=0, y=0, z=0),
                    material=Material(
                        colour=Colour(r=0, g=0, b=0),
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
                Ray(origin=Point(x=0, y=0, z=1), direction=Point(0, 0, 1)),
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
