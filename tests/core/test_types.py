import pytest

from raytracer.core.types import Vector


class TestVector:
    def test_magnitude(self):
        vector = Vector(x=1.0, y=-2.0, z=-2.0)
        actual = vector.magnitude
        assert actual == 3

    def test_dot_product(self):
        vector_1 = Vector(x=1.0, y=-2.0, z=-2.0)
        vector_2 = Vector(x=1.0, y=1.5, z=1.0)
        actual = vector_1.dot_product(other=vector_2)
        assert actual == -4.0

    def test_addition(self):
        vector_1 = Vector(x=1.0, y=-2.0, z=-2.0)
        vector_2 = Vector(x=2.0, y=-1.0, z=1.5)
        expected = Vector(x=3.0, y=-3.0, z=-0.5)
        actual = vector_1 + vector_2
        assert actual == expected

    def test_subtraction(self):
        vector_1 = Vector(x=1.0, y=-2.0, z=-2.0)
        vector_2 = Vector(x=2.0, y=-1.0, z=1.5)
        expected = Vector(x=-1.0, y=-1.0, z=-3.5)
        actual = vector_1 - vector_2
        assert actual == expected

    def test_multiply(self):
        vector = Vector(x=1.0, y=-2.0, z=-2.0)
        expected = Vector(x=3.0, y=-6.0, z=-6.0)
        actual = vector * 3
        assert actual == expected

    def test_multiply_by_another_vector_errors(self):
        vector_1 = Vector(x=1.0, y=-2.0, z=-2.0)
        vector_2 = Vector(x=2.0, y=-1.0, z=1.5)
        with pytest.raises(
            AssertionError, match="Cannot multiply a vector by another vector"
        ):
            vector_1 * vector_2

    def test_division(self):
        vector = Vector(x=1.0, y=-2.0, z=-2.0)
        expected = Vector(x=0.5, y=-1.0, z=-1.0)
        actual = vector / 2
        assert actual == expected

    def test_division_by_another_vector_errors(self):
        vector_1 = Vector(x=1.0, y=-2.0, z=-2.0)
        vector_2 = Vector(x=2.0, y=-1.0, z=1.5)
        with pytest.raises(
            AssertionError, match="Cannot divide a vector by another vector"
        ):
            vector_1 / vector_2

    def test_normalize(self):
        vector_1 = Vector(x=1.0, y=-2.0, z=-2.0)
        vector_2 = Vector(x=1.0, y=1.5, z=1.0)
        expected = Vector(
            x=0.48507125007266594, y=-0.9701425001453319, z=-0.9701425001453319
        )
        actual = vector_1.normalize(other=vector_2)
        assert actual == expected
