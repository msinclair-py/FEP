
mol delete all
mol load psf ../ini/ionized.psf pdb ../ini/ionized.pdb
set all [atomselect top all]
$all set occupancy 0
$all set beta      0

set C  [atomselect top "protein and name CA"]
set ligand1 [atomselect top "resname G6P BG6 and resid 1"]
set ligand3 [atomselect top "resname G6P BG6 and resid 2"]
$ligand1 set beta 1
$ligand3 set beta 1
$C set beta 1

$all writepdb min.pdb

$all set beta 0
set ligand1 [atomselect top "resname G6P BG6 and resid 1 and name P"]
set ligand3 [atomselect top "resname G6P BG6 and resid 2 and name P"]
$ligand1 set beta 1
$ligand3 set beta 1
$C set beta 1

$all writepdb restraints.pdb
exit
