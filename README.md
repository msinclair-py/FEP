# FEP
Workflow for running, analyzing and plotting Free Energy Perturbation (FEP) simulations using the NAMD MD engine.

1. Navigate to ini/
	- Ensure your input system is equilibrated and solvated (~30ns).
    - Run `ini_0.tcl` script to generate a second copy of your ligand in the bulk solvent. Note that you will need 
        to update this script to ensure the ligand placement is appropriate for your system (not outside the box, at
        least 2 times your non-bonded interaction cutoff away from protein, etc.)
	- May need to desolvate and then resolvate/ionize system after generation of second ligand if serious clashes or 
        instabilities not resolved by step 3 minimization.

2. Navigate to restraints/
    - Run `restraints.tcl` to generate restraint files for both system minimization and FEP runs. The protein should be
        restrained throughout simulation as well as 1 or more ligand atoms to ensure the ligand stays in one place but
        that it is still able to explore the conformational space.

3. Navigate to min/
    - Run minimization using sample configuration file `min.conf`. Note that you will need to make sure your ligand
        parameters are called in this config file.
    - After minimizing run `ini.tcl` to extract the minimized structure for input in the actual FEP runs.

4. Navigate to run/ 
	- Run setup.sh for a fresh run.
	- Load restart.xsc from the minimization.
	- Add ligand parameters to toppar.
	- If restarting runs, use clean.sh.
    - All sample jobscripts are configured for SGE job scheduler to run on a DGX2 machine, but can easily be modified for SLURM
        or other computational architectures.

5. Post running:
	- Run check.py to ensure that everything has ran to completion.
	- Run join.py to merge all FEP runs so that ParseFEP can analyze.
    - Using the Analyze FEP Simulation module in VMD>Extensions>Analysis, set the temperature accordingly, Gram-Charlier expansion
        order to 0 and attach your forward and backward fep files for analysis, selecting BAR estimator for error estimation.
    - Run plotFEP.py to generate plots of a single or even multiple FEP simulations. See ArgumentParser in plotFEP for arguments
        that the script takes and how to run it.

6. Additional caveats, notes and thoughts:
    - Modify min.conf to include equilibration location and cgenff parameters (.str).
    - Modify .conf files in run/ folder as necessary.
    - Entropy modification is generally unneccessary since it is negligibly small and may be within FEP error.
    - Error term will shift delta G values, but shouldn't affect delta delta G for comparing different FEP runs.
