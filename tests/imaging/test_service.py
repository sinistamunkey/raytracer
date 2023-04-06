import io

from raytracer.imaging.service import ImageService
from raytracer.imaging.types import Canvas


class TestImageService:
    def test_render(self) -> None:
        image_service = ImageService()
        canvas = Canvas(width=3, height=3)
        img_file = io.StringIO()
        image_service.render(canvas=canvas, image_file=img_file)
        actual = img_file.getvalue()
        expected = (
            "P3 3 3\n"
            "255\n"
            "0 0  0 0 0  0 0 0  0\n"
            "0 0  0 0 0  0 0 0  0\n"
            "0 0  0 0 0  0 0 0  0\n"
        )
        assert actual == expected
