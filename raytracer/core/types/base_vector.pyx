import math


cdef class BaseVector:
    cdef public float x
    cdef public float y
    cdef public float z

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self):
        return math.sqrt(self.dot_product(self))

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        return self / self.magnitude

    def __add__(self, other):
        return BaseVector(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other):
        return BaseVector(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __mul__(self, other):
        if not isinstance(self, BaseVector):
            return other.__mul__(self)
        return BaseVector(x=self.x * other, y=self.y * other, z=self.z * other)

    def __truediv__(self, other):
        return BaseVector(
            x=self.x / other,
            y=self.y / other,
            z=self.z / other,
        )

    def __eq__(self, other):
        if not isinstance(other, BaseVector):
            raise TypeError("Not supported")
        return all([self.x == other.x, self.y == other.y, self.z == other.z])

    def __repr__(self):
        return f"BaseVector({self.x}, {self.y}, {self.z})"

    @staticmethod
    def from_object(data):
        return BaseVector(x=data["x"], y=data["y"], z=data["z"])
