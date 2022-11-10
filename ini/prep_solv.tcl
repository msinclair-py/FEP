#################################################
set dir /Scr/msincla01/g6pc1/CORRECT_PROTONATION/Docked/beta_glucose/Run1
mol load psf $dir/g6pc1.psf
mol addfile $dir/g6pc1.pdb waitfor all

set all     [atomselect top "not water and not ions"]

$all writepsf desolv.psf
$all writepdb desolv.pdb

package require solvate
package require autoionize

solvate desolv.psf desolv.pdb -minmax {{-49 -49 -52} {49 49 52}} -o complex.sol
autoionize -psf complex.sol.psf -pdb complex.sol.pdb -sc 0.15 -o complex.sol.ion
mol delete all
exit
