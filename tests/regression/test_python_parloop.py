from __future__ import absolute_import, print_function, division
import numpy as np
import pytest

from firedrake import *


def test_python_parloop():

    m = UnitSquareMesh(4, 4)
    fs = FunctionSpace(m, "CG", 2)
    f = Function(fs)

    class MyExpression(Expression):
        def eval(self, value, X):

            value[:] = np.dot(X, X)

    f.interpolate(MyExpression())
    X = m.coordinates
    assert assemble((f-dot(X, X))**2*dx)**.5 < 1.e-15


def test_python_parloop_vector():

    m = UnitSquareMesh(4, 4)
    fs = VectorFunctionSpace(m, "CG", 1)
    f = Function(fs)

    class MyExpression(Expression):
        def eval(self, value, X):

            value[:] = X

        def value_shape(self):
            return (2,)

    f.interpolate(MyExpression())
    X = m.coordinates
    assert assemble((f - X)**2*dx)**.5 < 1.e-15


def test_python_parloop_vector_1D():

    m = UnitIntervalMesh(4)
    fs = VectorFunctionSpace(m, "CG", 1)
    f = Function(fs)

    class MyExpression(Expression):
        def eval(self, value, X):

            value[:] = X

        def value_shape(self):
            return (1,)

    f.interpolate(MyExpression())
    X = m.coordinates
    assert assemble((f - X)**2*dx)**.5 < 1.e-15


def test_python_parloop_user_kwarg():
    m = UnitSquareMesh(4, 4)
    fs = FunctionSpace(m, "CG", 2)
    f = Function(fs)

    class MyExpression(Expression):
        def eval(self, value, X, t=None):
            value[:] = t

    f.interpolate(MyExpression(t=10.0))

    assert np.allclose(assemble(f*dx), 10.0)


def test_python_parloop_vector_user_kwarg():
    m = UnitSquareMesh(4, 4)
    fs = VectorFunctionSpace(m, "CG", 1)
    f = Function(fs)

    class MyExpression(Expression):
        def eval(self, value, X, b=None, a=None):
            value[0] = a
            value[1] = b

        def value_shape(self):
            return (2,)

    f.interpolate(MyExpression(a=1.0, b=2.0))

    exact = Function(fs)
    exact.interpolate(Expression(("1.0", "2.0")))

    assert np.allclose(assemble((f - exact)**2*dx), 0.0)


if __name__ == '__main__':
    import os
    pytest.main(os.path.abspath(__file__))
