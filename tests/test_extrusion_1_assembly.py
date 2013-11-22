"""Tests for successful assembly of forms on extruded meshes"""
import pytest

from firedrake import *
from common import *

CG = [("CG", 1), ("CG", 2)]
DG = [("DG", 0), ("DG", 1)]
hdiv = [("RT", 1), ("RT", 2), ("RT", 3), ("BDM", 1)]


@pytest.mark.parametrize(('hfamily', 'hdegree', 'vfamily', 'vdegree'),
                         [(f, d, vf, vd) for (vf, vd) in CG + DG for (f, d) in CG + DG])
def test_scalar_assembly(hfamily, hdegree, vfamily, vdegree):
    mesh = extmesh(4, 4, 2)
    fspace = FunctionSpace(mesh, hfamily, hdegree, vfamily=vfamily, vdegree=vdegree)

    u = TrialFunction(fspace)
    v = TestFunction(fspace)

    assemble(u*v*dx).M._force_evaluation()
    assemble(dot(grad(u), grad(v))*dx).M._force_evaluation()


# two valid combinations for hdiv: 1) BDM/RT x DG, 2) DG x CG
@pytest.mark.parametrize(('hfamily', 'hdegree', 'vfamily', 'vdegree'),
                         [(f, d, vf, vd) for (vf, vd) in DG for (f, d) in hdiv]
                         + [(f, d, vf, vd) for (vf, vd) in CG for (f, d) in DG])
def test_hdiv_assembly(hfamily, hdegree, vfamily, vdegree):
    mesh = extmesh(4, 4, 2)

    horiz_elt = FiniteElement(hfamily, "triangle", hdegree)
    vert_elt = FiniteElement(vfamily, "interval", vdegree)
    product_elt = HDiv(OuterProductElement(horiz_elt, vert_elt))
    fspace = FunctionSpace(mesh, product_elt)

    u = TrialFunction(fspace)
    v = TestFunction(fspace)

    assemble(dot(u, v)*dx).M._force_evaluation()
    assemble(inner(grad(u), grad(v))*dx).M._force_evaluation()


# two valid combinations for hcurl: 1) BDM/RT x CG, 2) CG x DG
@pytest.mark.parametrize(('hfamily', 'hdegree', 'vfamily', 'vdegree'),
                         [(f, d, vf, vd) for (vf, vd) in CG for (f, d) in hdiv]
                         + [(f, d, vf, vd) for (vf, vd) in DG for (f, d) in CG])
def test_hcurl_assembly(hfamily, hdegree, vfamily, vdegree):
    mesh = extmesh(4, 4, 2)

    horiz_elt = FiniteElement(hfamily, "triangle", hdegree)
    vert_elt = FiniteElement(vfamily, "interval", vdegree)
    product_elt = HCurl(OuterProductElement(horiz_elt, vert_elt))
    fspace = FunctionSpace(mesh, product_elt)

    u = TrialFunction(fspace)
    v = TestFunction(fspace)

    assemble(dot(u, v)*dx).M._force_evaluation()
    assemble(inner(grad(u), grad(v))*dx).M._force_evaluation()

if __name__ == '__main__':
    import os
    pytest.main(os.path.abspath(__file__))