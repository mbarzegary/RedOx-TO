import firedrake as fd
from firedrake import sqrt, jump, dS, dx


def pde_filter(GAMMA, gamma, dim, filter_radius, solver_parameters):
    mesh = GAMMA.ufl_domain()
    if dim == 2:
        x, y = fd.SpatialCoordinate(mesh)
    elif dim == 3:
        x, y, z = fd.SpatialCoordinate(mesh)
    af, b = fd.TrialFunction(GAMMA), fd.TestFunction(GAMMA)
    x_ = fd.interpolate(x, GAMMA)
    y_ = fd.interpolate(y, GAMMA)
    if dim == 3:
        z_ = fd.interpolate(z, GAMMA)

    if dim == 2:
        Delta_h = sqrt(jump(x_) ** 2 + jump(y_) ** 2)
    elif dim == 3:
        Delta_h = sqrt(jump(x_) ** 2 + jump(y_) ** 2 + jump(z_) ** 2)
    aH = filter_radius**2 * jump(af) / Delta_h * jump(b) * dS + af * b * dx
    LH = gamma * b * dx

    gammaf = fd.Function(GAMMA, name="gamma")

    fd.solve(aH == LH, gammaf, solver_parameters=solver_parameters)

    return gammaf
