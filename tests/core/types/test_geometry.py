from typing import Type, TypeVar, cast

import pytest
from pytest import FixtureRequest

from raytracer.core.types.geometry import BaseVector, Point, Vector

BV = TypeVar("BV", bound=BaseVector)


class TestVector:
    @pytest.fixture(name="vector_cls", params=[Vector, Point])
    def vector_cls(self, request: FixtureRequest) -> Type[BV]:
        """
        Ensures that any test using this fixture is iterated
        for each of the "params" - in this case for any entity
        inheriting from `BaseVector`.
        """
        return cast(Type[BV], request.param)

    def test_magnitude(self, vector_cls: Type[BV]) -> None:
        vector = vector_cls(x=1.0, y=-2.0, z=-2.0)
        actual = vector.magnitude
        assert actual == 3

    def test_dot_product(self, vector_cls: Type[BV]) -> None:
        vector_1 = vector_cls(x=1.0, y=-2.0, z=-2.0)
        vector_2 = vector_cls(x=1.0, y=1.5, z=1.0)
        actual = vector_1.dot_product(other=vector_2)
        assert actual == -4.0

    def test_addition(self, vector_cls: Type[BV]) -> None:
        vector_1 = vector_cls(x=1.0, y=-2.0, z=-2.0)
        vector_2 = vector_cls(x=2.0, y=-1.0, z=1.5)
        expected = vector_cls(x=3.0, y=-3.0, z=-0.5)
        actual = vector_1 + vector_2
        assert actual == expected

    def test_subtraction(self, vector_cls: Type[BV]) -> None:
        vector_1 = vector_cls(x=1.0, y=-2.0, z=-2.0)
        vector_2 = vector_cls(x=2.0, y=-1.0, z=1.5)
        expected = vector_cls(x=-1.0, y=-1.0, z=-3.5)
        actual = vector_1 - vector_2
        assert actual == expected

    def test_multiply(self, vector_cls: Type[BV]) -> None:
        vector = vector_cls(x=1.0, y=-2.0, z=-2.0)
        expected = vector_cls(x=3.0, y=-6.0, z=-6.0)
        actual = vector * 3
        assert actual == expected

    def test_rmultiply(self, vector_cls: Type[BV]) -> None:
        vector = vector_cls(x=1.0, y=-2.0, z=-2.0)
        expected = vector_cls(x=3.0, y=-6.0, z=-6.0)
        actual = 3 * vector
        assert actual == expected

    def test_division(self, vector_cls: Type[BV]) -> None:
        vector = vector_cls(x=1.0, y=-2.0, z=-2.0)
        expected = vector_cls(x=0.5, y=-1.0, z=-1.0)
        actual = vector / 2
        assert actual == expected

    def test_normalize(self, vector_cls: Type[BV]) -> None:
        vector_1 = vector_cls(x=1.0, y=-2.0, z=-2.0)
        expected = vector_cls(
            x=0.3333333333333333, y=-0.6666666666666666, z=-0.6666666666666666
        )
        actual = vector_1.normalize()
        assert actual == expected
