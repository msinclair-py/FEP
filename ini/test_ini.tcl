##################################################
#set dir /Scr/sepehr/prestin/ligands/stability/sal
load /Projects/jribeiro/psfgen_center/psfgen2.0_shared_object/libpsfgen.so
set dir /Scr/arango/PPAR-Meling/MEH_FEP/charmm-gui-4401690096/namd/1/complex
#set dir /Scr/arango/membrane_AA/sepehr_build_fep/mehp/ini
#mol load psf $dir/ini/ionized.psf
mol load psf $dir/complex.psf
mol addfile $dir/complex.pdb

#mol addfile $dir/equ_1/equ.2.dcd waitfor all


set all     [atomselect top "all"]
set ligand1 [atomselect top "resname LIG and resid 1"]

$all writepdb ini.pdb
$all writepsf ini.psf

$ligand1 moveby {27 27 27}
$ligand1 set resid 2 
$ligand1 writepdb ligand1.pdb
$ligand1 writepsf ligand1.psf
##################################################
##################################################
package require psfgen
psfcontext reset 

topology /Scr/arango/PPAR-Meling/MEH_FEP/charmm-gui-4401690096/namd/1/ligand.prm
topology /Scr/arango/PPAR-Meling/MEH_FEP/charmm-gui-4401690096/namd/toppar/par_all36_cgenff.prm
topology /Scr/arango/PPAR-Meling/MEH_FEP/charmm-gui-4401690096/namd/toppar/par_all36m_prot.prm
topology /Scr/arango/PPAR-Meling/MEH_FEP/charmm-gui-4401690096/namd/toppar/toppar_water_ions.str
#topology ./Scr/arango/Aditi-Files/forJustin/simulating.drugs/par/toppar_water_ions_namd.str
topology /Scr/arango/PPAR-Meling/MEH_FEP/charmm-gui-4401690096/toppar/toppar_water_ions.str
topology /Scr/arango/PPAR-Meling/MEH_FEP/charmm-gui-4401690096/toppar/toppar_ions_won.str
readpsf ini.psf
readpsf ligand1.psf

coordpdb ini.pdb
coordpdb ligand1.pdb

writepsf ionized.psf
writepdb ionized.pdb
##################################################
##################################################
mol delete all
mol load psf ionized.psf pdb ionized.pdb
set all  [atomselect top all]
set sel1 [atomselect top "resname LIG and resid 1"]
set sel3 [atomselect top "resname LIG and resid 2"]

$all  set beta 0
$sel1 set beta -1
$sel3 set beta 1

$all writepdb fep.pdb
exit
