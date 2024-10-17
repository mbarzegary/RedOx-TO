from firedrake import *
parameters["reorder_meshes"] = False
from firedrake.adjoint import *
continue_annotation()

from pyMMAopt import MMASolver
from pyMMAopt import ReducedInequality
from pyadjoint.placeholder import Placeholder

from petsc4py import PETSc

import argparse
import os
import itertools

from pde_filter import pde_filter
from preconditioners import *
from helpers import *

from flow_problem import *
from charge_problem import *

def perform_topo_opt():

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--filter_radius", type=float, default=0.01)
    parser.add_argument("--porosity", type=float, default=0.5)
    parser.add_argument("--tau", type=float, default=0.5)
    parser.add_argument("--delta", type=float, default=15.0)
    parser.add_argument("--mu", type=float, default=5.0)
    parser.add_argument("--movlim", type=float, default=0.1)
    parser.add_argument("--maxiters", type=int, default=200)
    parser.add_argument("--output_dir", type=str, default="./results")
    parser.add_argument("--effective_porosity", type=str, default="simple")
    parser.add_argument("--dim", type=int, default=2)
    parser.add_argument("--forward", action="store_true", default=False)
    parser.add_argument("--mesh", type=str, default="normal") # "fine"
    parser.add_argument("--initial_gamma_value", type=float, default=0.5)
    parser.add_argument("--save_every", type=int, default=5)
    parser.add_argument("--Re", type=float, default=1.0)
    parser.add_argument("--Da", type=float, default=1e-4)
    parser.add_argument("--u_in", type=float, default=1.0)
    parser.add_argument("--flow_gls", action="store_true", default=False)
    parser.add_argument("--flow_ramp_p", type=float, default=2.0)
    # parser.add_argument("--flow_gamma_penalization", action="store_true", default=False)
    # parser.add_argument("--flow_gamma_penalization_type", type=str, default="ramp") # "ramp" "simp"
    parser.add_argument("--no_flow_objective_penalization", action="store_true", default=False)
    parser.add_argument("--flow_solver", type=str, default="iterative") # "direct" "iterative"
    parser.add_argument("--flow_objective", type=str, default="dissipation") # "pressure" "dissipation"
    parser.add_argument("--solve_stokes", action="store_true", default=False)
    parser.add_argument("--elec_contrib_ratio", type=float, default=1.0)
    parser.add_argument("--no_charge", action="store_true", default=False)
    parser.add_argument("--no_flow", action="store_true", default=False)

    args, _ = parser.parse_known_args()

    PETSc.Sys.Print(args)
    RH = args.filter_radius
    porosity = args.porosity
    effective_porosity = args.effective_porosity
    tau = args.tau
    delta = args.delta
    mu = args.mu
    movlim = args.movlim
    max_iters = args.maxiters
    output_dir = args.output_dir
    is_forward = args.forward
    save_every = args.save_every
    Re_val = args.Re
    Da_val = args.Da
    ramp_p_val = args.flow_ramp_p
    u_inflow = args.u_in
    use_GLS = args.flow_gls
    # penalize_gamma = args.flow_gamma_penalization
    penalize_flow_obj = not args.no_flow_objective_penalization
    flow_solver = args.flow_solver
    flow_objective = args.flow_objective
    solve_charge = not args.no_charge
    solve_flow = not args.no_flow
    solve_full_NS = not args.solve_stokes
    dim = args.dim
    mesh_type = args.mesh
    elec_contrib_ratio = args.elec_contrib_ratio
    initial_gamma_value = args.initial_gamma_value

    PETSc.Sys.Print(f'''
        Problem dimension: {dim}
        Solve charge: {solve_charge}
        Solve flow: {solve_flow}
        Output directory: {output_dir}
        Forward only: {is_forward}
        Save every: {save_every}

        Porosity: {porosity}
        Porosity correction: {effective_porosity}

        Tau: {tau}
        Delta: {delta}
        Mu: {mu}
        Contribution ratio of electric loss: {elec_contrib_ratio}

        Re: {Re_val}
        Darcy: {Da_val}
        Inlet velocity: {u_inflow}
        Full NS: {solve_full_NS}
        GLS: {use_GLS}
        Flow solver: {flow_solver}
        Flow objective: {flow_objective}
        Flow objective penalization: {penalize_flow_obj}
        RAMP value: {ramp_p_val}

        Max iterations: {max_iters}
        Filter radius: {RH}
        Move limit: {movlim}
        Initial gamma value: {initial_gamma_value}

        Mesh config: {mesh_type}
    ''')

    dump_args_dict(output_dir, args)

    if dim == 2:
        target_continuity = None
    elif dim ==3:
        target_continuity = H1 # to allow isocontours

    # Load mesh
    if dim == 2:
        if (mesh_type == "fine"):
            mesh = Mesh('mesh/electrode_in_out_top_thin_fine.msh')
        else:
            mesh = Mesh('mesh/electrode_in_out_top_thin.msh')
    elif dim == 3:
        if (mesh_type == "fine"):
            mesh = Mesh('mesh/electrode_in_out_top_thin_3D_fine.msh')
        else:
            mesh = Mesh('mesh/electrode_in_out_top_thin_3D.msh')

    # initial design
    GAMMA = FunctionSpace(mesh, "DG", 0)
    gamma = Function(GAMMA)
    with stop_annotating():
        gamma.interpolate(Constant(initial_gamma_value))

    # filtering
    if dim == 2:
        helmholtz_parameters = lu
    else:
        helmholtz_parameters = cg_hypre
    gammaf = pde_filter(GAMMA, gamma, dim, RH, helmholtz_parameters)
    gammafControl = Control(gammaf)

    # forward problem
    V = FunctionSpace(mesh, "CG", 1)
    W = V*V

    Vflow = VectorFunctionSpace(mesh, "CG", 2)
    Qflow = FunctionSpace(mesh, "CG", 1)
    Wflow = Vflow * Qflow

    ramp_p = Constant(ramp_p_val)
    Re = Constant(Re_val)
    Da = Constant(Da_val)
    Placeholder(Da)

    PETSc.Sys.Print(f"MPI Size: {COMM_WORLD.size}")
    PETSc.Sys.Print(f"No. of DoF in charge problem: {W.dim()}")
    PETSc.Sys.Print(f"No. of DoF in flow problem: {Wflow.dim()}\n")

    solver_parameters = snes_newtonls
    if dim == 2:
        solver_parameters.update(lu)
    else:
        solver_parameters.update(cg_pc_triang_hypre)

    if solve_charge:
        u, i_n = charge_problem(W, gammaf, delta, mu, tau, effective_porosity, porosity, boundary_conditions, solver_parameters)
        (Phi1sol, Phi2sol) = split(u)

    if solve_flow:
        up_forward = flow_problem(
            Wflow,
            1-gammaf,
            Re,
            Da,
            ramp_p,
            boundary_conditions,
            u_inflow,
            ramp,
            use_GLS,
            dim,
            solve_full_NS,
            solver_parameters = parLSC if flow_solver == "iterative" else parDIR
        )
        u_f, p = split(up_forward)
        up_control_f = Control(up_forward)

    def calculate_electric_loss():
        J = assemble(Constant(0) * ds(boundary_conditions["MEMBRANE"], domain=mesh))
        if solve_charge:
            J = assemble(Phi2sol * ds(boundary_conditions["MEMBRANE"]))
        return J

    def calculate_flow_loss():
        J = assemble(Constant(0) * ds(boundary_conditions["MEMBRANE"], domain=mesh))
        if solve_flow:
            if flow_objective == "dissipation":
                G = power_dissipation(u_f, 1-gammaf, Re, Da, penalization=ramp, ramp_p=ramp_p)
                J = G
                if penalize_flow_obj:
                    Wf = 1.0
                    J = J + assemble(Wf
                        * alpha(1-gammaf, Da, penalization=ramp, ramp_p=ramp_p)
                        * inner(u_f, u_f)
                        * dx(regions["DOMAIN"])
                    )
            else: # pressure drop
                J = assemble(p * ds(boundary_conditions["INLET"])) # / assemble(Constant(1.0)*ds(boundary_conditions["INLET"], domain=mesh))
        return J
    if solve_charge:
        J_initial = float(calculate_electric_loss())
    else:
        J_initial = 1
    if solve_flow:
        Power_initial = float(calculate_flow_loss())
    else:
        Power_initial = 1

    # optimization problem
    if is_forward == False:
        c = Control(gamma)

        gamma_viz_f = Function(GAMMA, name="gamma")
        controls_f = File(f"{output_dir}/control_iterations_f.pvd", target_continuity=target_continuity)
        if solve_flow:
            vel_pvd = File(f"{output_dir}/velocity.pvd")

        global_counter = itertools.count()

        J = calculate_electric_loss()
        J  = J / J_initial
        J_control = Control(J)

        Power = calculate_flow_loss()
        Power = Power / Power_initial
        Power_control = Control(Power)

        def deriv_cb(j, dj, gamma):
            iter = next(global_counter)
            with stop_annotating():
                if save_every != 0 and iter % save_every == 0:
                    # PETSc.Sys.Print(f"######### {iter}")
                    gamma_viz_f.assign(gammafControl.tape_value())
                    par_loop(
                        ("{[i] : 0 <= i < f.dofs}", "f[i, 0] = 0.0"),
                        dx(regions["IN_DOMAIN"]),
                        {"f": (gamma_viz_f, WRITE)}
                    )
                    par_loop(
                        ("{[i] : 0 <= i < f.dofs}", "f[i, 0] = 0.0"),
                        dx(regions["OUT_DOMAIN"]),
                        {"f": (gamma_viz_f, WRITE)}
                    )
                    gamma_viz_f.rename("Gamma")
                    controls_f.write(gamma_viz_f)
                    if solve_flow:
                        u_plot, p_plot = up_control_f.tape_value().subfunctions
                        u_plot.rename("Velocity")
                        p_plot.rename("Pressure")
                        vel_pvd.write(u_plot, p_plot)
                record_losses(output_dir, iter, J_control.tape_value(), Power_control.tape_value())
            return dj

        Jhat = ReducedFunctional(elec_contrib_ratio*J + Power, c, derivative_cb_post=deriv_cb)
        # Jhat = ReducedFunctional(J, c, derivative_cb_post=deriv_cb)

        Vol = assemble((1-gammaf) * dx(regions["DOMAIN"]))
        VolControl = Control(Vol)
        Volhat = ReducedFunctional(Vol, c)
        Vollimit = 1.0 * assemble(Constant(1.0) * dx(regions["DOMAIN"], domain=mesh))
        # Vollimit = 0.7 * assemble(Constant(1.0) * dx(regions["DOMAIN"], domain=mesh))

        problem = MinimizationProblem(Jhat, bounds=(0.0, 1.0), constraints=[ReducedInequality(Volhat, Vollimit, VolControl)])

        parameters_mma = {
            "move": movlim,
            "maximum_iterations": max_iters,
            "m": 1,
            "IP": 0,
            "tol": 1e-7,
            "accepted_tol": 1e-5,
            # "gcmma": True,
            "norm": "L2",
        }
        solver = MMASolver(problem, parameters=parameters_mma)

        results = solver.solve()
        gamma_opt = results["control"]

        gamma.assign(gamma_opt)
        gammaf.assign(gammafControl.tape_value())

        if solve_charge:
            u, i_n = charge_problem(W, gammaf, delta, mu, tau, effective_porosity, porosity, boundary_conditions, solver_parameters)

    par_loop(
        ("{[i] : 0 <= i < f.dofs}", "f[i, 0] = 0.0"),
        dx(regions["IN_DOMAIN"]),
        {"f": (gammaf, WRITE)}
    )
    par_loop(
        ("{[i] : 0 <= i < f.dofs}", "f[i, 0] = 0.0"),
        dx(regions["OUT_DOMAIN"]),
        {"f": (gammaf, WRITE)}
    )
    # File(f"{output_dir}/gamma.pvd", target_continuity=target_continuity).write(gamma)
    File(f"{output_dir}/gammaf.pvd", target_continuity=target_continuity).write(gammaf)

    if solve_charge:
        (Phi1vec, Phi2vec) = split(u)
        File(f"{output_dir}/solid_potential.pvd", target_continuity=target_continuity).write(Function(V, name="solid potential").interpolate(Phi1vec))
        File(f"{output_dir}/liquid_potential.pvd", target_continuity=target_continuity).write(Function(V, name="Ionic potential").interpolate(Phi2vec))
        File(f"{output_dir}/current_density.pvd", target_continuity=target_continuity).write(Function(V, name="Current density").interpolate(i_n))
        File(f"{output_dir}/current_density_indomain.pvd", target_continuity=target_continuity).write(Function(V, name="Current density").interpolate(i_n*gammaf))

    if solve_flow:
        vel_final_pvd = File(f"{output_dir}/velocity_final.pvd")
        u_plot, p_plot = up_control_f.tape_value().subfunctions
        u_plot.rename("Velocity")
        p_plot.rename("Pressure")
        vel_final_pvd.write(u_plot, p_plot)


if __name__ == "__main__":
    perform_topo_opt()
