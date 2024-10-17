lu = {
   "mat_type": "aij",
   "ksp_type": "preonly",
   "pc_type": "lu",
   }
cg_hypre = {"mat_type": "aij",
      "ksp_rtol": 1e-4,
      "ksp_type": "cg",
      "pc_type": "hypre",
      }

snes_newtonls = {"snes_type": "newtonls",
                  "snes_linesearch_type": "l2",
                  #"snes_converged_reason": None,
                  "snes_monitor": None,
                  "snes_rtol": 1e-4,
                  "snes_max_it": 50,
               }
cg_pc_triang_hypre = {"mat_type": "aij",
                  "ksp_rtol": 1e-4,
                  "ksp_type": "cg",
                  #"ksp_converged_reason": None,
                  "pc_type": "fieldsplit",
                  "pc_fieldsplit_type": "symmetric_multiplicative",
                  "fieldsplit_1_ksp_type": "preonly",
                  "fieldsplit_1_pc_type": "hypre",
                  "fieldsplit_0_ksp_type": "preonly",
                  "fieldsplit_0_pc_type": "hypre",
                  }

parLSC = {
       "ksp_type": "fgmres",
    #    "ksp_gmres_restart":150,
       "snes_monitor":None,
       "ksp_monitor":None,
      #  "ksp_atol":5e-7,
       "ksp_atol":5e-6,
       "snes_converged_reason":None,
    #    "ksp_gmres_modifiedgramschmidt":True,
       "pc_type": "fieldsplit",
       "pc_fieldsplit_type":"schur",
       "pc_fieldsplit_schur_fact_type":"full",
       "fieldsplit_0":{
           "ksp_type":"preonly",
           "pc_type":"gamg",
        #    "pc_lsc_factor_mat_solver_type": "mumps",
                      },
       "fieldsplit_1":{
        #    "ksp_type":"preonly",
           "pc_type":"jacobi",
           "ksp_max_it":5,
        #    "lsc_pc_type":"lu",
                      }
       }

# parLSC = {  # Stokes based on FF example
#        "ksp_type": "fgmres",
#        "snes_monitor":None,
#        "ksp_monitor":None,
#       #  "ksp_atol":5e-7,
#        "ksp_rtol":1e-6,
#        "snes_converged_reason":None,
#        "pc_type": "fieldsplit",
#        "pc_fieldsplit_type": "schur",
#        "pc_fieldsplit_schur_fact_type": "lower",
#        "pc_fieldsplit_detect_saddle_point": None,
#        "fieldsplit_0":{
#            "ksp_type": "gmres",
#            "pc_type": "lu",
#            "ksp_max_it":5,
#          #   "pc_factor_mat_solver_type": "mumps",
#                       },
#        "fieldsplit_1":{
#            "ksp_type": "gmres",
#            "pc_type":"lu",
#            "ksp_max_it":5,
#          #   "pc_factor_mat_solver_type": "mumps",
#                       }
#        }

# parLSC = { # Stokes from g-adopt repo
#     "mat_type": "matfree",
#     "snes_type": "ksponly",
#     "ksp_type": "preonly",
#     "pc_type": "fieldsplit",
#     "pc_fieldsplit_type": "schur",
#     "pc_fieldsplit_schur_type": "full",
#     "snes_monitor":None,
#     "ksp_monitor":None,
#     "fieldsplit_0": {
#         "ksp_type": "cg",
#         "ksp_rtol": 1e-5,
#         "pc_type": "python",
#         "pc_python_type": "firedrake.AssembledPC",
#         "assembled_pc_type": "gamg",
#         "assembled_pc_gamg_threshold": 0.01,
#         "assembled_pc_gamg_square_graph": 100,
#     },
#     "fieldsplit_1": {
#         "ksp_type": "fgmres",
#         "ksp_rtol": 1e-4,
#         "pc_type": "python",
#         "pc_python_type": "firedrake.MassInvPC",
#         "Mp_ksp_rtol": 1e-5,
#         "Mp_ksp_type": "cg",
#         "Mp_pc_type": "sor",
#     }
# }


parDIR = {
          "snes_monitor": None,
          "ksp_type": "preonly",
          "mat_type": "aij",
          "pc_type": "lu",
          "pc_factor_mat_solver_type": "mumps"
          }



parPCD = {
       "ksp_type":"fgmres",
       "mat_type":"matfree",
       "snes_monitor":None,
       "snes_converged_reason":None,
       "ksp_gmres_restart":800,
       "ksp_gmres_modifiedgramschmidt":None,
       "pc_type": "fieldsplit",
       "pc_fieldsplit_type":"schur",
       "pc_fieldsplit_schur_fact_type":"upper",
       "fieldsplit_0":{
           "ksp_type":"preonly",
           "pc_type":"python",
           "pc_python_type":"firedrake.AssembledPC",
           "assembled_mat_type":"aij",
           "assembled_pc_type":"lu",
           },
       "fieldsplit_1":{
           "ksp_type":"preonly",
           "pc_type":"python",
           "pc_python_type":"FPCD.PCD",

           # MASS MATRIX Mp = p*q*dx
           "pcd_Mp_ksp_type":"preonly",
           "pcd_Mp_pc_type":"lu",
 
           # STIFNESS MATRIX Kp = inner(grad(p),grad(q))*dx
           "pcd_Kp_ksp_type":"preonly",
           "pcd_Kp_pc_type": "lu",

           "pcd_Fp_mat_type":"matfree"
           },
      }  