#!/bin/bash
for (( i = 0; i < 50; i++ )); do

    DIR=f$i
	if [ ! -d "$DIR" ]; then
        mkdir f$i
	fi
    DIR=b$i
    if [ ! -d "$DIR" ]; then
        mkdir b$i
    fi
    echo "$i out of 50"
done
mkdir f_out_0 f_out_1 f_out_2 f_out_3
mkdir b_out_0 b_out_1 b_out_2 b_out_3
