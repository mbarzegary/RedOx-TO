import itertools
import os
from datetime import datetime
import time
import argparse

def command_generator(sim_code, post_code, perform_sim, perform_post, loss_plot_only, *args_and_values):

    # Generate all possible combinations of parameter values
    parameter_combinations = list(itertools.product(*[values if isinstance(values, list) else [values] for _, values in args_and_values]))

    counter = itertools.count()
    commands = []

    for combination in parameter_combinations:
        comb_num = next(counter)
        sim_cmd_args = ""
        post_cmd_args = ""
        for (param_name, _), param_value in zip(args_and_values, combination):
            if param_name == "output_dir":
                # Special handling for output directory
                param_value = f"{str(param_value)}/run{comb_num}"
                post_cmd_args = f' --input_dir {str(param_value)} --out_name postprocess/run{comb_num}'
            sim_cmd_args += f" --{str(param_name)} {str(param_value)}"

        if perform_sim:
            # Generate simulation command
            commands.append(sim_code + sim_cmd_args + f" 2>&1 | tee logs/run{comb_num}.log")

        if perform_post:
            # Generate post-processing command
            if loss_plot_only:
                post_cmd_args += " --loss_plot_only"
            commands.append(post_code + post_cmd_args + f" 2>&1 | tee logs/run{comb_num}-post.log")

    return commands

if __name__ == "__main__":

    # Set up command-line argument parser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--sim_only", action="store_true", default=False)
    parser.add_argument("--post_only", action="store_true", default=False)
    parser.add_argument("--loss_plot_only", action="store_true", default=False)
    parser.add_argument("--dry_run", action="store_true", default=False)

    args, _ = parser.parse_known_args()
    perform_sim = not args.post_only
    perform_post = not args.sim_only
    loss_plot_only = args.loss_plot_only
    run_commands = not args.dry_run # Run or just generate (dry run)

    # Configuration parameters
    num_proc = 6
    include_num_proc = False # False for some HPC environments

    mpi_cmd = "srun " # "mpirun --use-hwthread-cpus " "mpiexec " "srun " ("" for serial run)
    sim_code = "python optimization.py"
    post_code = "python postprocess.py"

    if include_num_proc:
        mpi_cmd += f"-n {num_proc} "
    sim_code = mpi_cmd + sim_code

    # Define parameter values for the parameter sweep
    output_dir_values = "./results"
    porosity_values = 0.5
    tau_values = [0.5, 0.1, 0.005]
    delta_values = [1.0, 25.0]
    mu_values = [0.1, 5.0]
    maxiters_values = 150
    effective_porosity_values = "effective" # ["simple", "effective"]
    dim_values = 2
    mesh_values = "fine" # "normal" for debug, "fine" for main
    save_every_values = 0
    Re_values = 1.0
    Da_values = [1e-4, 5e-4, 1e-5]
    u_in_values  = 1.0
    flow_solver_values = "direct" # "iterative"
    elec_contrib_ratio_values = [1.0, 2.0]
    # solve_stokes
    # no_flow
    # no_charge

    # Generate commands for all parameter combinations
    commands = command_generator(sim_code, post_code, perform_sim, perform_post, loss_plot_only,
                                                    ("porosity", porosity_values),
                                                    ("tau", tau_values),
                                                    ("delta", delta_values),
                                                    ("mu", mu_values),
                                                    ("maxiters", maxiters_values),
                                                    ("effective_porosity", effective_porosity_values),
                                                    ("dim", dim_values),
                                                    ("mesh", mesh_values),
                                                    ("save_every", save_every_values),
                                                    ("Re", Re_values),
                                                    ("Da", Da_values),
                                                    ("u_in", u_in_values),
                                                    ("flow_solver", flow_solver_values),
                                                    ("elec_contrib_ratio", elec_contrib_ratio_values),
                                                    ("output_dir", output_dir_values),
                                                    )
    # print(commands)

    # Create directory for command lists if it doesn't exist
    cmd_list_dir = f"./commands"
    if not os.path.exists(cmd_list_dir):
        os.makedirs(cmd_list_dir)
    
    # Generate timestamp for unique file naming
    ts = datetime.timestamp(datetime.now())
    date_time = datetime.fromtimestamp(ts)
    timestamp = date_time.strftime("%Y-%m-%d-%H:%M:%S")

    # Write commands to file
    with open(f'{cmd_list_dir}/commands-{timestamp}.txt', 'w') as f:
        f.write('\n'.join(commands))

    if run_commands:
        # Create directories for output
        os.makedirs("postprocess", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        for cmd in commands:
            print(f"RUNNING: {cmd}")
            start = time.time()
            os.system(cmd)
            # Record execution time for each command
            with open(f'{cmd_list_dir}/commands-{timestamp}_time.txt', "a+") as f:
                f.write(f"{time.time()-start:.0f} seconds\n")
