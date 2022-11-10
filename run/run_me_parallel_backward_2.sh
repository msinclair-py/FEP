#!/bin/bash

qsub -q dgx -N fep.back2 -j y -o ~/Jobs << EOF
cd "$PWD"

/Projects/jmaia/Repo/namd_devel_2/namd/GPU_Replica/charmrun ++local /Scr/jmaia/Binaries/dev_current/namd/Linux-x86_64-icc-sn-netlrts/namd3 +p16 +replicas 16 +devicesperreplica 1 backward_parallel.2.conf +stdout ./b_out_2/b%d.out > backward.2.log 

EOF
