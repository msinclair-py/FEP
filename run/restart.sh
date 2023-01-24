#!/bin/bash

dir=${1}
num=${2}

log="${dir}${num}"

cp restart_single_window.conf RESTART.conf
sed -i "s/DIRECTION/$dir/" RESTART.conf
sed -i "s/WINDOW/$num/" RESTART.conf

qsub -q gpu -N fep.rest -j y -o /Scr/msincla01/Jobs << EOF
cd "$PWD"
namd3 RESTART.conf > $log/RESTART.log

EOF
