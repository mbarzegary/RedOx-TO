import os
from petsc4py import PETSc
from firedrake import COMM_WORLD
import json

boundary_conditions = {
    "INLET": 1,
    "OUTLET": 2,
    "WALLS": 3,
    "CURRENT_COLLECTOR": 4,
    "MEMBRANE": 5,
}

regions = {
    "DOMAIN": 5,
    "IN_DOMAIN": 6,
    "OUT_DOMAIN": 7
}

shape_params = {
    "INLET_WIDTH": 0.3,
    "X_INLET": 0.3
}

def dump_args_dict(output_dir, args):
    if COMM_WORLD.rank == 0:
        data_output_dir = f"{output_dir}/data"
        if not os.path.exists(data_output_dir):
            os.makedirs(data_output_dir)
        with open(f'{data_output_dir}/args.json', 'w') as json_file:
            json.dump(vars(args), json_file)

def record_losses(output_dir, iteration, elec_loss, flow_loss):
    PETSc.Sys.Print(f"##### Total loss {elec_loss + flow_loss}")
    PETSc.Sys.Print(f"##### Electric loss {elec_loss}")
    PETSc.Sys.Print(f"##### Flow loss {flow_loss}")
    if COMM_WORLD.rank == 0:
        data_output_dir = f"{output_dir}/data"
        if not os.path.exists(data_output_dir):
            os.makedirs(data_output_dir)
        f = open(f"{data_output_dir}/losses.txt", "a+")
        if iteration == 0:
            f.write("iter\telec\tflow\ttotal\n")
        f.write(f"{iteration}\t{elec_loss}\t{flow_loss}\t{elec_loss+flow_loss}\n")
        f.close()