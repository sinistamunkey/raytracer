from raytracer.core.types.imaging import Canvas, Colour


class TestColour:
    def test_addition(self) -> None:
        colour_1 = Colour(r=30, g=23, b=99)
        colour_2 = Colour(r=4, g=12, b=33)
        expected = Colour(r=34, g=35, b=132)
        actual = colour_1 + colour_2
        assert actual == expected

    def test_addition_max_values(self) -> None:
        colour_1 = Colour(r=255, g=255, b=255)
        colour_2 = Colour(r=4, g=12, b=33)
        expected = Colour(r=255, g=255, b=255)
        actual = colour_1 + colour_2
        assert actual == expected

    def test_subtraction(self) -> None:
        colour_1 = Colour(r=30, g=23, b=99)
        colour_2 = Colour(r=4, g=12, b=33)
        expected = Colour(r=26, g=11, b=66)
        actual = colour_1 - colour_2
        assert actual == expected

    def test_subtraction_min_values(self) -> None:
        colour_1 = Colour(r=0, g=0, b=0)
        colour_2 = Colour(r=4, g=12, b=33)
        expected = Colour(r=0, g=0, b=0)
        actual = colour_1 - colour_2
        assert actual == expected

    def test_multiply(self) -> None:
        colour = Colour(r=1, g=2, b=3)
        expected = Colour(r=2, g=4, b=6)
        actual = colour * 2
        assert actual == expected

    def test_division(self) -> None:
        colour_1 = Colour(r=20, g=40, b=60)
        expected = Colour(r=10, g=20, b=30)
        actual = colour_1 / 2
        assert actual == expected

    def test_rounds_floats(self) -> None:
        actual = Colour(r=1.5, g=2.3, b=6.9)  # type: ignore
        expected = Colour(r=2, g=2, b=7)
        assert actual == expected

    def test_from_hex(self) -> None:
        actual = Colour.from_hex("#FF0000")
        expected = Colour(r=255, g=0, b=0)
        assert actual == expected


class TestCanvas:
    def test_paint(self) -> None:
        canvas = Canvas(width=2, height=2)
        pixel = Colour(r=33, g=12, b=111)
        canvas.paint(x=1, y=1, pixel=pixel)
        assert canvas.pixels[1][1] == pixel
