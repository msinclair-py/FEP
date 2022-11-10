
proc loadtraj {PSFFILE DCDFILES START N STEP} {
    mol delete all
    mol load psf $PSFFILE
    for {set i $START} {$i < $N} {incr i} {
        if {[file exists $DCDFILES.$i.dcd] } {
            mol addfile $DCDFILES.$i.dcd waitfor all step $STEP
        }
    }
}
proc loadtraj_C {DCDFILES START N STEP} {
    for {set i $START} {$i < $N} {incr i} {
        if {[file exists $DCDFILES.$i.dcd] } {
            mol addfile $DCDFILES.$i.dcd waitfor all step $STEP
        }
    }
}

set STEP     10

mol load psf ../ini/ionized.psf
for {set i 0} {$i < 50} {incr i} {
    mol addfile ../run/b$i/b$i.dcd waitfor all step 10
}
for {set i 0} {$i < 50} {incr i} {
    mol addfile ../run/f$i/f$i.dcd waitfor all step 10
}


set nframes [molinfo top get numframes]
set OUPOUT [open COM.txt w]

animate goto 0


for {set i 0} {$i < $nframes} {incr i 1} {
    
    set ligand1 [atomselect top "resname BG6 and resid 0" frame $i]

    puts "frame $i of $nframes" 
    set COM1 [measure center $ligand1 weight mass]
    set x1 [lindex $COM1 0]
    set y1 [lindex $COM1 1]
    set z1 [lindex $COM1 2]

    puts $OUPOUT "$i $x1 $y1 $z1"; flush stdout
}
close $OUPOUT


exit
