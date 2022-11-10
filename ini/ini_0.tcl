##################################################
mol load psf input.psf
mol addfile input.pdb waitfor all
#mol addfile $dir/1.pdb

set all     [atomselect top "all"]
set ligand1 [atomselect top "resname G6P BG6 and resid 1"]

$all writepdb ini.pdb
$all writepsf ini.psf

$ligand1 moveby {20 40 40}
$ligand1 set resid 2 
$ligand1 writepdb ligand1.pdb
$ligand1 writepsf ligand1.psf
##################################################
##################################################
package require topotools
set midlist {}

set mol [mol new ini.psf]
mol addfile ini.pdb $mol
lappend midlist $mol

set mol [mol new ligand1.psf]
mol addfile ligand1.pdb $mol
lappend midlist $mol

set mol [::TopoTools::mergemols $midlist]
animate write psf ionized.psf $mol
animate write pdb ionized.pdb $mol

##################################################
##################################################
mol delete all
mol load psf ionized.psf pdb ionized.pdb
set all  [atomselect top all]
set sel1 [atomselect top "resname G6P BG6 and resid 1"]
set sel3 [atomselect top "resname G6P BG6 and resid 2"]

$all  set beta 0
$sel1 set beta -1
$sel3 set beta 1

$all writepdb fep.pdb
exit
