import numpy as np

class NormalPoint:
    """Normalised Cartesian coördinates"""
    def __init__(self, x, y):
        self.x, self.y = x, y
    def polar(t):
        return NormalPoint(np.cos(t), np.sin(t))
    def null():
        return NormalPoint(0, 0)
    def low():
        return NormalPoint(-1, -1)
    def high():
        return NormalPoint(1, 1)
    def xy(self):
        return (self.x, self.y)
    def quadrature(self):
        return self.x**2 + self.y**2
    def norm(self):
        return np.sqrt(self.quadrature())
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    def angle(self, other=None):
        if other is None: other = NormalPoint(1, 0)
        return np.arccos(self.dot(other) / (self.norm() * other.norm()))
    def binary(self, op, other):
        return NormalPoint(op(self.x, other.x), op(self.y, other.y))
    def __add__(self, other):
        return self.binary(lambda a, b: a + b, other)
    def __sub__(self, other):
        return self.binary(lambda a, b: a - b, other)
    def __mul__(self, other):
        return self.binary(lambda a, b: a * b, other)
    def __div__(self, other):
        return self.binary(lambda a, b: a / b, other)
    def __neg__(self):
        return NormalPoint.null() - self
    def __repr__(self):
        return f"({self.x}, {self.y})"

# The following shape primitives are predicate functions
# which indicate if a point (in normalised space) is inside
# the shape (True), or outside (False).
# The shapes do not take any dimensions, since the will occupy the
# most amount of space available to them in the [-1; 1]×[-1; 1] ⊆ ℝ²
# normalised space.

def circle(p):
    """Unit circle in normalised space"""
    return p.quadrature() <= 1

def square(p):
    """Fills the entire normal space"""
    return True

def rectangle(p, ratio):
    """Rectangle given aspect-ratio (width:height)"""
    if ratio == 1: # square
        return True
    if ratio > 1:  # wider than tall
        return -1/ratio <= p.y <= 1/ratio
    return -ratio <= p.x <= ratio

def polygon(p, vertices):
    """Regular convex n-sided ploygon"""
    # The angles subtended across the polygon edges from
    # the perspective of the point, should sum to be 2π if
    # the point is inside the polygon, otherwise it is not.
    epsilon = 0.01
    turns = len(vertices)
    if vertices[-1] == vertices[0]:  # polygon is already closed
        turns -= 1
    angles = sum((p - vertices[i]).angle(p - vertices[i - 1]) for i in range(turns))
    return np.abs(angles - 2*np.pi) < epsilon

def regular_polygon(p, sides):
    corners = np.vectorize(NormalPoint.polar)(np.linspace(-np.pi / 2, 2*np.pi * (3/4 - 1/sides), sides))
    return polygon(p, corners)

def triangle(p):
    return regular_polygon(p, 3)

def diamond(p):
    return regular_polygon(p, 4)

def pentagon(p):
    return regular_polygon(p, 5)

def hexagon(p):
    return regular_polygon(p, 6)

def star_of_david(p):
    """Two triangles superimposed."""
    # The logical union (or) acts as the union of
    # the set of points in both shapes.
    return triangle(p) or triangle(-p)

def ascii_draw(shape):
    bg, fg = ' ', '#'
    w, h = 90, 40

    for y in np.linspace(-1, 1, h):
        for x in np.linspace(-1, 1, w):
            p = NormalPoint(x, y)
            print(fg if shape(p) else bg, end='')
        print('\n', end='')


def shape_init(shape, corner, w, h, size):
    array = np.array([np.ones(size[0]) for _ in range(size[1])])

    for j in np.arange(corner, h+corner, 1):
        for i in np.arange(corner, w+corner, 1):
            y = 2*(j-corner)/h-1
            x = 2*(i-corner)/w-1
            p = NormalPoint(y, x)

            if shape(p):
                array[i, j] = -1
    return array


#ascii_draw(circle)

## To draw pretty pictures with these, take them out of normalised
## space, translate them around, and create a scene out of multiple of them.
## Write to a 2D array by making a function that takes a shape, a scale, and
## a position to place it in, and put it in the lattice by writing the appropriate
## values to the correct indices.
