from __future__ import absolute_import, print_function, division
import pytest
import numpy as np
from firedrake import *


def test_manual_quadrature():
    mesh = UnitSquareMesh(4, 4)
    V = FunctionSpace(mesh, "CG", 3)
    f = Function(V).interpolate(Expression("pow(x[0], 3)"))

    f1 = f*dx(degree=3)
    f2 = f*dx(degree=1)
    f3 = f*dx

    assert np.allclose(assemble(f1), assemble(f3))

    assert np.allclose(assemble(f1), 0.25)

    assert np.allclose(assemble(f2), 0.244791666666)

    assert np.allclose(assemble(f1) + assemble(f2), assemble(f1 + f2))


if __name__ == "__main__":
    import os
    pytest.main(os.path.abspath(__file__))
