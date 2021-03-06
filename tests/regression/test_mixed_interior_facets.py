from __future__ import absolute_import, print_function, division
import pytest
from firedrake import *


@pytest.fixture(scope='module')
def mesh2D():
    # .---.
    # |\  |
    # | \ |
    # |  \|
    # '---'
    return UnitSquareMesh(1, 1)


@pytest.mark.parametrize('degree', [1, 2, 3])
def test_vfs(mesh2D, degree):
    V = VectorFunctionSpace(mesh2D, 'CG', degree)
    u = Function(V)
    u.interpolate(Expression(('1.0', '1.0')))
    n = FacetNormal(mesh2D)

    # Unit '+' normal is (1, 1)/sqrt2, and diagonal has length sqrt2.
    assert abs(assemble(dot(u('-'), n('-'))*dS) + 2.0) < 1e-10
    assert abs(assemble(dot(u('+'), n('-'))*dS) + 2.0) < 1e-10
    assert abs(assemble(dot(u('+'), n('+'))*dS) - 2.0) < 1e-10

    u.interpolate(Expression(('1.0', '-1.0')))
    assert abs(assemble(dot(u('+'), n('+'))*dS)) < 1e-10


def test_mfs(mesh2D):
    V1 = FunctionSpace(mesh2D, 'BDM', 1)
    V2 = FunctionSpace(mesh2D, 'CG', 2)
    V3 = FunctionSpace(mesh2D, 'CG', 3)
    W = V3 * V1 * V2
    u = project(Expression(('1.0', '-1.0', '-1.0', '1.0')), W)
    n = FacetNormal(mesh2D)

    # Unit '+' normal is (1, 1)/sqrt2, and diagonal has length sqrt2.
    # This is (dot((1, 1), n+) + 10*dot((-1, -1), n-)) * dS = 2 + 20 = 22
    a = (u[0]('+')*n[0]('+') + u[3]('-')*n[1]('+')
         + 10*u[1]('+')*n[0]('-') + 10*u[2]('-')*n[1]('-'))*dS

    assert abs(assemble(a) - 22.0) < 1e-9


if __name__ == '__main__':
    import os
    pytest.main(os.path.abspath(__file__))
