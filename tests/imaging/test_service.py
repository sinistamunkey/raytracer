import io
import os
from unittest.mock import Mock, call

import pytest
from pytest_mock import MockerFixture

from raytracer.core.types.imaging import Canvas
from raytracer.imaging.service import ImageService


@pytest.fixture
def canvas() -> Canvas:
    return Canvas(width=3, height=3)


class TestImageService:
    def test_render(self, canvas: Canvas) -> None:
        """
        GIVEN a canvas
        AND an image file stream
        WHEN calling render
        THEN render the image to the file stream
        """
        image_service = ImageService()

        img_file = io.StringIO()
        image_service._render(canvas=canvas, image_file=img_file)
        actual = img_file.getvalue()
        expected = (
            "P3 3 3\n"
            "255\n"
            "0 0  0 0 0  0 0 0  0\n"
            "0 0  0 0 0  0 0 0  0\n"
            "0 0  0 0 0  0 0 0  0\n"
        )
        assert actual == expected

    def test_render_updates_progress(self, canvas: Canvas) -> None:
        """
        GIVEN a canvas
        AND an image file stream
        AND an update function
        WHEN calling render
        THEN call the update function when writing a line
        """
        # GIVEN
        image_service = ImageService()
        update_func = Mock()
        img_file = io.StringIO()

        # WHEN
        image_service._render(
            canvas=canvas, image_file=img_file, update_func=update_func
        )

        # THEN
        update_func.assert_has_calls([call(1), call(1), call(1)])

    def test_save_and_convert(self, canvas: Canvas, temp_directory: str) -> None:
        """
        GIVEN a canvas
        AND a filepath
        AND the filepath is a JPEG file
        WHEN calling save
        THEN convert the image to a JPEG
        """
        # GIVEN
        image_service = ImageService()

        # WHEN
        filepath = os.path.join(temp_directory, "testing.jpeg")
        actual = image_service.save(canvas=canvas, filepath=filepath)

        # THEN
        assert os.path.exists(filepath)
        assert actual == filepath

    def test_save_no_convert(
        self, canvas: Canvas, temp_directory: str, mocker: MockerFixture
    ) -> None:
        """
        GIVEN a canvas
        AND a filepath
        BUT the filepath is a PPM file
        WHEN calling save
        THEN don't convert the file
        """
        # GIVEN
        image_service = ImageService()
        mock_image = mocker.patch("raytracer.imaging.service.Image")

        # WHEN
        filepath = os.path.join(temp_directory, "testing.ppm")
        actual = image_service.save(canvas=canvas, filepath=filepath)

        # THEN
        assert os.path.exists(filepath)
        assert actual == filepath
        assert mock_image.mock_calls == []

    def test_save_invalid_format(self, canvas: Canvas, temp_directory: str) -> None:
        """
        GIVEN a canvas
        AND a filepath
        BUT the filepath has an unhandled extension
        WHEN calling save
        THEN raise an error
        """
        # GIVEN
        image_service = ImageService()
        filepath = os.path.join(temp_directory, "testing.wtf")

        # WHEN
        with pytest.raises(ValueError, match="'.wtf' is not a valid ImageFormat"):
            image_service.save(canvas=canvas, filepath=filepath)
