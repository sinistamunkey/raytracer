from typing import Self


class Loadable:
    @classmethod
    def from_object(cls, data: dict) -> Self:
        raise NotImplementedError  # pragma:nocover
