#!/usr/bin/env python
import os, shutil
from tqdm import trange

N = 50 # number of FEP windows

try:
    shutil.copyfile('b0/b0.fepout', 'backward.fepout')
    shutil.copyfile('f0/f0.fepout', 'forward.fepout')
except:
    pass

def join_files(direction: str) -> None:
    f = open(f'{direction}.fepout', 'a')
    d = direction[0]

    for i in trange(1, 50):
        tmp = open(f'{d}{i}/{d}{i}.fepout', 'r').readlines()[2:]

        for line in tmp:
            f.write(line)

join_files('backward')
join_files('forward')
