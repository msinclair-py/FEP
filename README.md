# FEP
Workflow for running, analyzing and plotting Free Energy Perturbation (FEP) simulations using the NAMD MD engine.

Steps to get absolute FEP going

1. Go to ini/ and run ini_0.tcl
	- you'll have to modify the script to move your ligand to the bulk solvent
	- make sure your input system is equilibrated and solvated (~30ns)
	- may need to desolvate and then resolvate/ionize system if serious clashes or instabilities not
      resolved by step 3 minimizatin

2. Go to restraints/ and run  

3. Go to min/ and minimize your new system 

4. Go to run/ 
	- run setup.sh for a fresh run
	- load restart.xsc from the minimization
	- add ligand parameters to toppar
	- if restarting runs, use clean.sh
    - All sample jobscripts are configured for SGE job scheduler but can easily be modified for SLURM

5. Post running:
	- Run check.py to ensure that everything has ran
	- Run join.py to merge all FEP runs so that ParseFEP can analyze.
    - Run plotFEP.py to generate plots of a single or even multiple FEP simulations

Additional caveats, notes and thoughts:
modify min.conf to include equlibration location and cgenff parameters (.str)

modify .conf files in run/ folder 

Entropy modification is unneccessary since it is negligibly small and may be within FEP error
Error term will shift delta G values, but shouldn't affect delta delta G
