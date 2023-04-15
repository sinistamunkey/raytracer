from raytracer.core.types.imaging import Canvas, Colour


class TestColour:
    def test_addition(self) -> None:
        colour_1 = Colour(30, 23, 99)
        colour_2 = Colour(4, 12, 33)
        expected = Colour(34, 35, 132)
        actual = colour_1 + colour_2
        assert actual == expected

    def test_addition_max_values(self) -> None:
        colour_1 = Colour(255, 255, 255)
        colour_2 = Colour(4, 12, 33)
        expected = Colour(255, 255, 255)
        actual = colour_1 + colour_2
        assert actual == expected

    def test_subtraction(self) -> None:
        colour_1 = Colour(30, 23, 99)
        colour_2 = Colour(4, 12, 33)
        expected = Colour(26, 11, 66)
        actual = colour_1 - colour_2
        assert actual == expected

    def test_subtraction_min_values(self) -> None:
        colour_1 = Colour(0, 0, 0)
        colour_2 = Colour(4, 12, 33)
        expected = Colour(0, 0, 0)
        actual = colour_1 - colour_2
        assert actual == expected

    def test_multiply(self) -> None:
        colour = Colour(1, 2, 3)
        expected = Colour(2, 4, 6)
        actual = colour * 2
        assert actual == expected

    def test_rmultiply(self) -> None:
        colour = Colour(1, 2, 3)
        expected = Colour(2, 4, 6)
        actual = 2 * colour
        assert actual == expected

    def test_division(self) -> None:
        colour_1 = Colour(20, 40, 60)
        expected = Colour(10, 20, 30)
        actual = colour_1 / 2
        assert actual == expected

    def test_rounds_floats(self) -> None:
        actual = Colour(1.5, 2.3, 6.9)  # type: ignore
        expected = Colour(2, 2, 7)
        assert actual == expected

    def test_from_hex(self) -> None:
        actual = Colour.from_hex("#FF0000")
        expected = Colour(255, 0, 0)
        assert actual == expected


class TestCanvas:
    def test_paint(self) -> None:
        canvas = Canvas(width=2, height=2)
        pixel = Colour(33, 12, 111)
        canvas.paint(x=1, y=1, pixel=pixel)
        assert canvas.pixels[1][1] == pixel
