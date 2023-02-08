#!/usr/bin/env python
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotting_methods import *

parser = argparse.ArgumentParser()

parser.add_argument('filepath', help='Filepath to individual FEP run directories.\
                    If no systems argument is passed this should be where the \
                    results directory is contained, which holds the ParseFEP.log\
                    file.', default=os.getcwd())
parser.add_argument('-s', '--systems', dest='systems', help='Space delimited string\
                    which corresponds to all systems to be analyzed. Note that each\
                    system ought to be contained in the `filepath` directory using\
                    the standard FEP template directory structure.')
parser.add_argument('--simple', dest='_default', help='Set this flag to if you are \
                    not plotting from the traditional FEP architecture. E.g. if the \
                    ParseFEP.log file is in just a bare directory.', action='store_false')
parser.set_defaults(_default=True)

args = parser.parse_args()
filepath = args.filepath

if filepath[-1] == '/':
    filepath = filepath[:-1]

try:
    names = args.systems.split(' ')
except AttributeError:
    names = ''

_default = args._default

systems = [os.path.join(filepath, system) for system in names]
n = len(systems)

assert n < 11, f'ERROR: colormap only contains 10 color combinations \
                    but you provided {n} systems!'

df = compile_all_data(systems, names, _default)
colors = get_colorscheme(n)

plot_paths(df, n, colors)
ddG = plot_ddG(df, n, names, colors[::3])

plt.show()
