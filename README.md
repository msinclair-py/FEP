# FEP
Workflow for running, analyzing and plotting Free Energy Perturbation (FEP) simulations using the NAMD MD engine.

Steps to get absolute FEP going:
1. Go to ini/ 
    - Run `ini_0.tcl`
	- Ensure your input system is equilibrated and solvated (~30ns)
	- May need to desolvate and then resolvate/ionize system if serious clashes or instabilities not
      resolved by step 3 minimization

2. Go to restraints/
    - Run `restraints.tcl` 

3. Go to min/
    - Run minimization using sample configuration file `min.conf`
    - After minimizing run `ini.tcl` to extract the minimized structure for the actual FEP runs

4. Go to run/ 
	- Run setup.sh for a fresh run
	- Load restart.xsc from the minimization
	- Add ligand parameters to toppar
	- If restarting runs, use clean.sh
    - All sample jobscripts are configured for SGE job scheduler but can easily be modified for SLURM

5. Post running:
	- Run check.py to ensure that everything has ran
	- Run join.py to merge all FEP runs so that ParseFEP can analyze.
    - Run plotFEP.py to generate plots of a single or even multiple FEP simulations

Additional caveats, notes and thoughts:
    - Modify min.conf to include equilibration location and cgenff parameters (.str)
    - Modify .conf files in run/ folder as necessary
    - Entropy modification is unneccessary since it is negligibly small and may be within FEP error
    - Error term will shift delta G values, but shouldn't affect delta delta G
