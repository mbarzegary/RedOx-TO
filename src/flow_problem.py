from firedrake import *
from penalization import ramp
from helpers import *

def inflow(u_inflow, dim, W):
    # Define the inflow boundary condition
    mesh = W.ufl_domain()
    if dim == 2:
        x, y = SpatialCoordinate(mesh)
    elif dim == 3:
        x, y, z = SpatialCoordinate(mesh)

    # Return the inflow velocity vector based on dimension
    if dim == 2:
        return as_vector(
            [
                0.0,
                u_inflow * sin(((x - (shape_params["X_INLET"])) * pi) / shape_params["INLET_WIDTH"])
            ]
        )
    else:
        return as_vector(
            [
                0.0,
                0.0,
                u_inflow * sin(((x - (shape_params["X_INLET"])) * pi) / shape_params["INLET_WIDTH"])
            ]
        )

def alpha(rho, Da, penalization=ramp, ramp_p=10.0):
    return (
        # Constant(1.0) / Da / rho
        Constant(1.0) / Da * penalization(rho, ramp_p=ramp_p, val_0=1.0, val_1=0.0)
    )

def GLS(u, v, p, q, rhof, Da, Re, penalization=ramp, ramp_p=10.0):
    """
    Outside of design domain DOMAIN:
    GLS = tau_gls * inner(R_U, theta_u) * dx(OUTSIDE)
    Inside of design domain
    GLS = tau_gls_alpha * inner(R_U + R_U_alpha, theta_U + theta_U_alpha) * dx(DOMAIN)
    """
    R_U = dot(u, grad(u)) - 1.0 / Re * div(grad(u)) + grad(p)
    R_U_alpha = alpha(rhof, Da, penalization=penalization, ramp_p=ramp_p) * u
    theta_U = dot(u, grad(v)) - 1.0 / Re * div(grad(v)) + grad(q)
    theta_U_alpha = alpha(rhof, Da, penalization=penalization, ramp_p=ramp_p) * v
    mesh = rhof.function_space().ufl_domain()
    h = CellDiameter(mesh)

    beta_gls = 0.5
    # beta_gls = 30.0
    tau_gls = Constant(beta_gls) * (
        (4.0 * dot(u, u) / h ** 2) + 9.0 * (4.0 / (Re * h ** 2)) ** 2
    ) ** (-0.5)
    tau_gls_alpha = Constant(beta_gls) * (
        (4.0 * dot(u, u) / h ** 2)
        + 9.0 * (4.0 / (Re * h ** 2)) ** 2
        + (alpha(rhof, Da, penalization=penalization, ramp_p=ramp_p)) ** 2
    ) ** (-0.5)

    return tau_gls * inner(R_U, theta_U) * (
        dx(regions["IN_DOMAIN"]) + dx(regions["OUT_DOMAIN"])
    ) + tau_gls_alpha * inner(R_U + R_U_alpha, theta_U + theta_U_alpha) * dx(regions["DOMAIN"])

def flow_problem(
    W,
    rhof,
    Re,
    Da,
    ramp_p,
    boundary_conditions,
    u_inflow,
    penalization,
    use_GLS,
    dim,
    solve_full_NS,
    solver_parameters=None):
    # Define test functions
    v, q = TestFunctions(W)

    # Define the trial functions
    up = Function(W)
    u, p = split(up)

    # Define the variational form
    F = (
        1.0 / Re * inner(grad(u), grad(v)) * dx
        + (inner(dot(grad(u), u), v) * dx  if solve_full_NS else 0) # switch between NS and Stokes
        - p * div(v) * dx
        + div(u) * q * dx
        + alpha(rhof, Da, penalization=penalization, ramp_p=ramp_p)
        * inner(u, v)
        * dx(regions["DOMAIN"])
    )

    # Add GLS stabilization if enabled
    if use_GLS:
        F = F + GLS(u, v, p, q, rhof, Da, Re, penalization=penalization, ramp_p=ramp_p)

    # Define no-slip boundary condition
    if dim == 2:
        noslip = Constant((0.0, 0.0))
    else:
        noslip = Constant((0.0, 0.0, 0.0))

    # Set up boundary conditions
    bcs_1 = DirichletBC(W.sub(0), noslip, [boundary_conditions["WALLS"],
                                            boundary_conditions["CURRENT_COLLECTOR"],
                                            boundary_conditions["MEMBRANE"]])
    
    inflow_forward = inflow(u_inflow, dim, W)
    bcs_2 = DirichletBC(W.sub(0), inflow_forward, boundary_conditions["INLET"])

    bcs = [bcs_1, bcs_2]

    # Set up and solve the problem
    problem = NonlinearVariationalProblem(F, up, bcs=bcs)
    solver = NonlinearVariationalSolver(problem, solver_parameters=solver_parameters)
    solver.solve()

    return up

def power_dissipation(u, rhof, Re, Da, penalization, ramp_p):
    return assemble(
        1.0 / Re * inner(grad(u), grad(u)) * dx
        + alpha(rhof, Da, penalization=penalization, ramp_p=ramp_p)
        * inner(u, u)
        * dx(regions["DOMAIN"])
    )