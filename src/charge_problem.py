from firedrake import *
from helpers import *

def charge_problem(
    W,
    gammaf,
    delta,
    mu,
    tau,
    effective_porosity,
    porosity,
    boundary_conditions,
    solver_parameters=None,
):
    u = Function(W)
    (Phi1, Phi2) = split(u)
    (p1,p2) = TestFunctions(W)

    factor_porosity = 1.0 if effective_porosity == "simple" else 0.0736806299  # 0.02^(2/3)
    porosity_new = porosity * factor_porosity
    epsilon_new = (1-gammaf) + (gammaf)*porosity_new
    epsilon = (1-gammaf) + (gammaf)*porosity
    a = gammaf 

    DPhi = Phi1 - Phi2
    sigma = (1-epsilon)**1.5 + 1e-22
    kappa = epsilon_new**1.5 + 1e-22

    bc = DirichletBC(W.sub(0), Constant(0), [boundary_conditions["CURRENT_COLLECTOR"]])
    bcs = [bc]

    i_n = exp(mu * DPhi) - exp(-mu * DPhi)
    g2 = Constant(1)

    a1 = inner(sigma*grad(Phi1), grad(p1))*dx + delta / mu * tau/(1+tau) * a * i_n * p1 * dx
    a2 = tau * inner(kappa*grad(Phi2), grad(p2))*dx - delta / mu * tau / (1+tau) * a * i_n * p2 * dx - tau * g2 * p2 * ds(boundary_conditions["MEMBRANE"])


    F = a1 + a2

    solve(F == 0, u, bcs = bcs, solver_parameters = solver_parameters)

    return u, i_n
