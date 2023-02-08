#!/bin/bash

dir=${1}
num=${2}

log="${dir}${num}"

if [ "$dir" = "f" ]
then
    cp restart_forward_window.conf RESTART.conf
elif [ "$dir" = "b" ]
then
    cp restart_backward_window.conf RESTART.conf
else
    echo "ERROR: Must provide direction as either `b` or `f`!"
    return -1
fi

sed -i "s/DIRECTION/$dir/" RESTART.conf
sed -i "s/WINDOW/$num/" RESTART.conf
rm -f ${dir}${num}/${dir}${num}.log

qsub -q gpu -N fep.rest -j y -o /Scr/msincla01/Jobs << EOF
cd "$PWD"
namd3 RESTART.conf > $log/${dir}${num}.log

EOF
