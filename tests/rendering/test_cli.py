import json
import os
from typing import Iterator
from unittest import mock
from unittest.mock import Mock, call, patch
from uuid import uuid4

import pytest
from click.testing import CliRunner

from raytracer.core.types.entities import Scene
from raytracer.core.types.imaging import Canvas
from raytracer.rendering.cli.render_scene import render_scene


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(autouse=True)
def config(temp_directory: str) -> Iterator[Mock]:
    with patch("raytracer.rendering.cli.render_scene.config") as mock_config:
        mock_config.OUT_DIR = temp_directory
        mock_config.SCENE_DIR = temp_directory
        yield mock_config


@pytest.fixture
def scene_file(temp_directory: str, scene_data: dict) -> str:
    scene_name = uuid4().hex
    filepath = os.path.join(temp_directory, f"{scene_name}.json")
    with open(filepath, mode="w") as f:
        json.dump(scene_data, f)
    return scene_name


@pytest.fixture
def canvas() -> Canvas:
    return Canvas(width=10, height=10)


@pytest.fixture(autouse=True)
def render_engine(canvas: Canvas) -> Iterator[Mock]:
    mock_engine = Mock(render=Mock(return_value=canvas))
    with patch(
        "raytracer.rendering.cli.render_scene.RenderEngine", return_value=mock_engine
    ):
        yield mock_engine


@pytest.fixture(autouse=True)
def image_service() -> Iterator[Mock]:
    mock_service = Mock(save=Mock(return_value="testing.ppm"))
    with patch(
        "raytracer.rendering.cli.render_scene.ImageService", return_value=mock_service
    ):
        yield mock_service


class TestRenderScene:
    def test_render_scene(
        self,
        config: Mock,
        cli_runner: CliRunner,
        scene_file: str,
        render_engine: Mock,
        image_service: Mock,
        scene_data: dict,
        canvas: Canvas,
    ) -> None:
        width = 320
        height = 240
        scene = Scene.from_object(data=scene_data, width=width, height=height)
        manager = Mock()
        manager.attach_mock(render_engine, "render_engine")
        manager.attach_mock(image_service, "image_service")

        result = cli_runner.invoke(
            render_scene,
            [
                "--filename",
                "testing.ppm",
                "--scene",
                scene_file,
                "--width",
                str(width),
                "--height",
                str(height),
            ],
        )

        assert result.exit_code == 0
        manager.assert_has_calls(
            [
                call.render_engine.render(scene=scene, update_func=mock.ANY),
                call.image_service.save(
                    canvas=canvas,
                    filepath=os.path.join(config.OUT_DIR, "testing.ppm"),
                    update_func=mock.ANY,
                ),
            ]
        )
