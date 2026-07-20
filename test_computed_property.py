import unittest
from math import sqrt

from computed_property import computed_property


class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color
        self.calls = 0

    @computed_property('x', 'y', 'z')
    def magnitude(self):
        self.calls += 1
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property('radius')
    def diameter(self):
        """Circle diameter from radius"""
        return self.radius * 2

    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2

    @diameter.deleter
    def diameter(self):
        self.radius = 0


class CircleComAreaInexistente:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property('radius', 'area')
    def diameter(self):
        return self.radius * 2


class TestComputedProperty(unittest.TestCase):

    def test_computa_uma_vez_e_cacheia(self):
        v = Vector(9, 2, 6)
        self.assertEqual(v.magnitude, 11.0)
        self.assertEqual(v.magnitude, 11.0)
        self.assertEqual(v.calls, 1)  # computou uma vez só

    def test_dependencia_nao_muda_mantem_cache(self):
        v = Vector(9, 2, 6)
        _ = v.magnitude
        v.color = 'red'  # nao é dependência
        _ = v.magnitude
        self.assertEqual(v.calls, 1)

    def test_dependencia_muda_recomputa(self):
        v = Vector(9, 2, 6)
        self.assertEqual(v.magnitude, 11.0)
        v.y = 18
        self.assertEqual(v.magnitude, 21.0)
        self.assertEqual(v.calls, 2)

    def test_dependencia_inexistente_ignorada(self):
        c = CircleComAreaInexistente()
        self.assertEqual(c.diameter, 2)
        self.assertEqual(c.diameter, 2)  # 'area' inexistente não quebra nem invalida

    def test_setter(self):
        c = Circle()
        self.assertEqual(c.diameter, 2)
        c.diameter = 3
        self.assertEqual(c.radius, 1.5)
        self.assertEqual(c.diameter, 3.0)  # recomputou após o setter mudar radius

    def test_deleter(self):
        c = Circle()
        del c.diameter
        self.assertEqual(c.radius, 0)

    def test_set_sem_setter_levanta_attributeerror(self):
        c = CircleComAreaInexistente()
        with self.assertRaises(AttributeError):
            c.diameter = 5

    def test_delete_sem_deleter_levanta_attributeerror(self):
        c = CircleComAreaInexistente()
        with self.assertRaises(AttributeError):
            del c.diameter

    def test_docstring_preservada(self):
        self.assertEqual(Circle.diameter.__doc__, "Circle diameter from radius")


if __name__ == '__main__':
    unittest.main()
