# Topology optimization framework for porous electrodes in electrochemical flow reactors

This repository contains a topology optimization framework for porous electrodes in  electrochemical flow cells. The framework solves combined flow and charge transport problems and is implemented in Python using the Firedrake and PETSc libraries for finite element modeling.

## Features

- Topology optimization for combined flow and charge transport problems
- Support for both 2D and 3D simulations
- Customizable problem parameters through command-line arguments
- Batch running capabilities for parameter sweeps
- Post-processing and visualization of results

## Structure

The main components of the framework are (under the `src` directory):

- `optimization.py`: Main optimization script
- `charge_problem.py`: Defines the charge transport problem
- `flow_problem.py`: Defines the flow problem (Navier-Stokes or Stokes)
- `batch_run.py`: Script for running multiple simulations with different parameters
- `postprocess.py`: Handles post-processing and visualization of (2D) results
- `helpers.py`: Contains helper functions and constants
- `preconditioners.py`: Defines various preconditioners and solver parameters
- `pde_filter.py`: Implements a PDE-based filter for the design variable
- `penalization.py`: Defines penalization schemes for topology optimization

## Usage

The `run_scripts` directory contains a few examples on how to use the framework in HPC environments. For local runs, you need to adjust the MPI binaries and arguments in `batch_run.py`.

<!-- For more details on available arguments, run the scripts with the `--help` flag. -->

## Requirements

This code requires the following software packages:

* [Firedrake](https://www.firedrakeproject.org/): Core finite element library used for solving PDEs, with features for automatic differentiation and parallel computing
* [pyadjoint](https://pyadjoint.org/): Automatic differentiation tool for adjoint analysis, installs with Firedrake
* [PETSc](https://petsc.org/) and [petsc4py](https://petsc.org/release/petsc4py/): Python bindings for PETSc (Portable, Extensible Toolkit for Scientific Computation)
* [pyMMAopt](https://github.com/LLNL/pyMMAopt): Python implementation of the Method of Moving Asymptotes (MMA) for optimization
* [ParaView](https://www.paraview.org/) (Python bindings): Visualization tool used for post-processing and generating images of results
* [PIL/Pillow](https://python-pillow.github.io/): Python Imaging Library for image manipulation in post-processing
* [Matplotlib](https://matplotlib.org/): Python plotting library used for creating loss function graphs
* [Gmsh](https://gmsh.info/): Meshing tool to generate the finite element mesh files required for the simulations

The code uses MPI for parallel execution.

<!--
## Publications

## License

## Contributors -->
