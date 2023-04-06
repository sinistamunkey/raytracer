from raytracer.core.types.imaging import Canvas, Pixel


class TestPixel:
    def test_addition(self) -> None:
        pixel_1 = Pixel(r=30, g=23, b=99)
        pixel_2 = Pixel(r=4, g=12, b=33)
        expected = Pixel(r=34, g=35, b=132)
        actual = pixel_1 + pixel_2
        assert actual == expected

    def test_addition_max_values(self) -> None:
        pixel_1 = Pixel(r=255, g=255, b=255)
        pixel_2 = Pixel(r=4, g=12, b=33)
        expected = Pixel(r=255, g=255, b=255)
        actual = pixel_1 + pixel_2
        assert actual == expected

    def test_subtraction(self) -> None:
        pixel_1 = Pixel(r=30, g=23, b=99)
        pixel_2 = Pixel(r=4, g=12, b=33)
        expected = Pixel(r=26, g=11, b=66)
        actual = pixel_1 - pixel_2
        assert actual == expected

    def test_subtraction_min_values(self) -> None:
        pixel_1 = Pixel(r=0, g=0, b=0)
        pixel_2 = Pixel(r=4, g=12, b=33)
        expected = Pixel(r=0, g=0, b=0)
        actual = pixel_1 - pixel_2
        assert actual == expected

    def test_multiply(self) -> None:
        pixel = Pixel(r=1, g=2, b=3)
        expected = Pixel(r=2, g=4, b=6)
        actual = pixel * 2
        assert actual == expected

    def test_division(self) -> None:
        pixel_1 = Pixel(r=20, g=40, b=60)
        expected = Pixel(r=10, g=20, b=30)
        actual = pixel_1 / 2
        assert actual == expected

    def test_rounds_floats(self) -> None:
        actual = Pixel(r=1.5, g=2.3, b=6.9)  # type: ignore
        expected = Pixel(r=2, g=2, b=7)
        assert actual == expected

    def test_from_hex(self) -> None:
        actual = Pixel.from_hex("#FF0000")
        expected = Pixel(r=255, g=0, b=0)
        assert actual == expected


class TestCanvas:
    def test_paint(self) -> None:
        canvas = Canvas(width=2, height=2)
        pixel = Pixel(r=33, g=12, b=111)
        canvas.paint(x=1, y=1, pixel=pixel)
        assert canvas.pixels[1][1] == pixel
