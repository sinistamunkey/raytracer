from raytracer.core.constants import MAX_COLOUR, MIN_COLOUR


cdef class Colour:
    cdef int _r
    cdef int _g
    cdef int _b

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @r.setter
    def r(self, value):
        self._r = self._clamp_value(value)

    @g.setter
    def g(self, value):
        self._g = self._clamp_value(value)

    @b.setter
    def b(self, value):
        self._b = self._clamp_value(value)

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return Colour(
            r=self.r + other.r,
            g=self.g + other.g,
            b=self.b + other.b,
        )

    def __sub__(self, other):
        return Colour(
            r=self.r - other.r,
            g=self.g - other.g,
            b=self.b - other.b,
        )

    def __eq__(self, other):
        if not isinstance(other, Colour):
            raise TypeError("Not supported")
        return all([self.r == other.r, self.g == other.g, self.b == other.b])

    def _clamp_value(self, value):
        return round(max(min(value, MAX_COLOUR), MIN_COLOUR))

    def __mul__(self, other):
        if not isinstance(self, Colour):
            return other.__mul__(self)
        return Colour(
            r=int(self.r * other), g=int(self.g * other), b=int(self.b * other)
        )

    def __truediv__(self, other):
        return Colour(
            r=int(self.r / other),
            g=int(self.g / other),
            b=int(self.b / other),
        )

    def __repr__(self):
        return f"Colour({self.r}, {self.g}, {self.b})"

    @staticmethod
    def from_hex(value):
        red = int(value[1:3], 16)
        green = int(value[3:5], 16)
        blue = int(value[5:7], 16)
        return Colour(r=red, g=green, b=blue)
