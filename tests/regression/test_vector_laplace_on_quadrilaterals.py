from __future__ import absolute_import, print_function, division
import numpy as np
import pytest

from firedrake import *


def vector_laplace(n, degree):
    mesh = UnitSquareMesh(n, n, quadrilateral=True)

    # spaces for calculation
    V0 = FunctionSpace(mesh, "CG", degree)
    V1 = FunctionSpace(mesh, "RTCE", degree)
    V = V0*V1

    # spaces to store 'analytic' functions
    W0 = FunctionSpace(mesh, "CG", degree + 1)
    W1 = VectorFunctionSpace(mesh, "CG", degree + 1)

    # constants
    k = 1.0
    l = 2.0

    f_expr = Expression(("pi*pi*(kk*kk + ll*ll)*sin(kk*pi*x[0])*cos(ll*pi*x[1])", "pi*pi*(kk*kk + ll*ll)*cos(kk*pi*x[0])*sin(ll*pi*x[1])"), kk=k, ll=l)
    exact_s_expr = Expression("-(kk+ll)*pi*cos(kk*pi*x[0])*cos(ll*pi*x[1])", kk=k, ll=l)
    exact_u_expr = Expression(("sin(kk*pi*x[0])*cos(ll*pi*x[1])", "cos(kk*pi*x[0])*sin(ll*pi*x[1])"), kk=k, ll=l)

    f = Function(W1).interpolate(f_expr)
    exact_s = Function(W0).interpolate(exact_s_expr)
    exact_u = Function(W1).interpolate(exact_u_expr)

    sigma, u = TrialFunctions(V)
    tau, v = TestFunctions(V)
    a = (sigma*tau - dot(u, grad(tau)) + dot(grad(sigma), v) + dot(curl(u), curl(v)))*dx
    L = dot(f, v)*dx

    out = Function(V)

    # preconditioner for H1 x H(curl)
    aP = (dot(grad(sigma), grad(tau)) + sigma*tau + dot(curl(u), curl(v)) + dot(u, v))*dx

    solve(a == L, out, Jp=aP,
          solver_parameters={'pc_type': 'fieldsplit',
                             'pc_fieldsplit_type': 'additive',
                             'fieldsplit_0_pc_type': 'lu',
                             'fieldsplit_1_pc_type': 'lu',
                             'ksp_monitor': True})

    out_s, out_u = out.split()

    return (sqrt(assemble(dot(out_u - exact_u, out_u - exact_u)*dx)),
            sqrt(assemble((out_s - exact_s)*(out_s - exact_s)*dx)))


@pytest.mark.parametrize(('testcase', 'convrate'),
                         [((1, (2, 4)), 0.9),
                          ((2, (2, 4)), 1.9),
                          ((3, (2, 4)), 2.9),
                          ((4, (2, 4)), 3.9)])
def test_hcurl_convergence(testcase, convrate):
    degree, (start, end) = testcase
    l2err = np.zeros((end - start, 2))
    for ii in [i + start for i in range(len(l2err))]:
        l2err[ii - start, :] = vector_laplace(2 ** ii, degree)
    assert (np.log2(l2err[:-1, :] / l2err[1:, :]) > convrate).all()


if __name__ == '__main__':
    import os
    pytest.main(os.path.abspath(__file__))
