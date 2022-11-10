#!/bin/bash
for (( i = 0; i < 50; i++ )); do

    cd ./b$i
    rm -f b$i.fepout.BAK
    cd ..
    cd ./f$i
    rm -f f$i.fepout.BAK
    cd ..

done
