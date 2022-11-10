#!/bin/bash

qsub -q dgx -N fep.forw3 -j y -o ~/Jobs << EOF
cd "$PWD"

/Projects/jmaia/Repo/namd_devel_2/namd/GPU_Replica/charmrun ++local /Scr/jmaia/Binaries/dev_current/namd/Linux-x86_64-icc-sn-netlrts/namd3 +p2 +replicas 2 +devicesperreplica 1 forward_parallel.3.conf +stdout ./f_out_3/f%d.out > forward.3.log  

EOF
