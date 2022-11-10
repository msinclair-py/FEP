#!/bin/bash

qsub -q dgx -N fep.forw1 -j y -o ~/Jobs << EOF
cd "$PWD"

/Projects/jmaia/Repo/namd_devel_2/namd/GPU_Replica/charmrun ++local /Scr/jmaia/Binaries/dev_current/namd/Linux-x86_64-icc-sn-netlrts/namd3 +p16 +replicas 16 +devicesperreplica 1 forward_parallel.1.conf +stdout ./f_out_1/f%d.out > forward.1.log  

EOF
