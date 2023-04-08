import os
import tempfile
from typing import Iterator

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from raytracer.imaging.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def temp_dir() -> Iterator[str]:
    with tempfile.TemporaryDirectory() as _tmp_dir:
        yield _tmp_dir


class TestBall:
    def test_returns_file_created(
        self, runner: CliRunner, mocker: MockerFixture, temp_dir: str
    ) -> None:
        # GIVEN
        config = mocker.patch("raytracer.imaging.cli.ball.config")
        config.OUT_DIR = temp_dir
        expected_file = os.path.join(temp_dir, "test.ppm")
        expected = f"Generated file: {expected_file}"

        # WHEN
        result = runner.invoke(
            cli, ["ball", "--width=10", "--height=10", "--filename=test.ppm"]
        )
        actual = result.output.strip()

        # THEN
        assert actual == expected
        assert os.path.exists(expected_file)

    def test_generates_random_filename_if_not_provided(
        self, runner: CliRunner, mocker: MockerFixture, temp_dir: str
    ) -> None:
        # GIVEN
        config = mocker.patch("raytracer.imaging.cli.ball.config")
        config.OUT_DIR = temp_dir

        # WHEN
        result = runner.invoke(cli, ["ball", "--width=10", "--height=10"])
        actual = result.output.strip()

        # THEN
        filename = actual.split(":")[-1].strip()
        assert os.path.exists(filename)
