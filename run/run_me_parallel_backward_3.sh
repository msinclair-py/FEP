#!/bin/bash

qsub -q dgx -N fep.back3 -j y -o ~/Jobs << EOF
cd "$PWD"

/Projects/jmaia/Repo/namd_devel_2/namd/GPU_Replica/charmrun ++local /Scr/jmaia/Binaries/dev_current/namd/Linux-x86_64-icc-sn-netlrts/namd3 +p2 +replicas 2 +devicesperreplica 1 backward_parallel.3.conf +stdout ./b_out_3/b%d.out > backward.3.log 

EOF
