
mol load psf ../ini/ionized.psf 
mol addfile forfep.dcd first -1 waitfor all

set all [atomselect top all]

$all writepdb ionized.pdb
$all writepsf ionized.psf

exit
