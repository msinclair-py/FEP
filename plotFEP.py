#!/usr/bin/env python
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

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
try:
    names = args.systems.split(' ')
except AttributeError:
    names = ''

_default = args._default

systems = [os.path.join(filepath, system) for system in names]
n = len(systems)

assert n < 11, f'ERROR: colormap only contains 10 color combinations \
                    but you provided {n} systems!'

def compile_all_data(systems, names, _default):
    if _default:
        dest = 'run/results/ParseFEP.log'
    else:
        dest = 'ParseFEP.log'

    df = pd.DataFrame()
    for i, (system, name) in enumerate(zip(systems, names)):
        temp = extract_data(f'{system}/{dest}')
        temp['system'] = name
        df = pd.concat([df, temp])
    
    df['hue'] = df['system'] + '-' + df['direction']
    return df.reset_index(drop=True)


def extract_data(logfile):
    lines = [line.strip() for line in open(logfile).readlines() if ':' in line]
    data = [line.split() for line in lines[:102]]
    bar = lines[-1].split()
    data.append(['free_energy:', '1', '0', bar[6], bar[-1]])
    
    dframe = pd.DataFrame(data, columns=['direction', 'lambda', 'ddA', 'dA', 'dSig'], 
                            dtype=float)
    dframe['direction'] = dframe['direction'].str[:-1]

    return dframe


def get_colorscheme(n):
    """
    For `n` different FEP systems, generate a colorscheme of matching saturated
    and light colors for various plots. Every 3rd element is a blank for use
    in the legend of the forward/backward plot so as to attach the dG information
    without an actual line.
    """
    sat_colors = ['tab:green', 'tab:red', 'royalblue', 'tan', 
                    'mediumorchid', 'chartreuse', 'xkcd:blush', 'maroon', 
                    'xkcd:pine green', 'goldenrod']
    light_cols = ['honeydew', 'xkcd:pastel pink', 'lightcyan',
                    'blanchedalmond', 'honeydew', 'thistle', 'xkcd:brick', 'mistyrose',
                    'xkcd:mint', 'cornsilk']
    colorscheme = [None] * 3 * n
    colorscheme[::3] = sat_colors[:n]
    colorscheme[1::3] = light_cols[:n]
    colorscheme[2::3] = ['white'] * n

    return colorscheme


def plot_paths(dframe, n, colors):
    fig, ax = plt.subplots(1,1, figsize=(8,5))
    style = ['-']*51 + ['--']*51 + ['x']
    style = style * n
    
    sns.lineplot(data=dframe, x='lambda', y='dA', hue='hue', style=style,
                    ax=ax, palette=colors)
    
    ax.set_xlabel('\u03BB', fontsize=20)
    ax.set_ylabel('\u0394G$_{binding}$ (kcal/mol)', fontsize=20)

    ymin = ((df['dA'].min() // 10) - 1) * 10
    ymax = ((df['dA'].max() // 10) + 1) * 10
    ax.set_ylim(ymin, ymax)
    
    h, l = ax.get_legend_handles_labels()
    labels = []
    for label in l[:-3]:
        if 'free_energy' in label:
            lab = f'{label.split("-")[0].capitalize()} \u0394G = '
            lab += f'{dframe.loc[dframe["hue"] == label, "dA"].values[0]:.2f}'
        else:
            lab = ' '.join([x.capitalize() for x in label.split('-')])

        labels.append(lab)

    legend = plt.legend(h[:-3], labels, bbox_to_anchor=(1, 1.05), prop={'size': 12})
    frame = legend.get_frame()
    frame.set_facecolor('xkcd:light grey')

    plt.tight_layout()
    plt.savefig('dG_lambda_forw_back.png', dpi=150)
    return fig


def plot_ddG(df, sat_colors, names):
    fig, ax = plt.subplots(1,1, figsize=(2,2))

    fe = df.loc[df['direction'] == 'free_energy', 'dA':'hue'].reset_index(drop=True)
    fe['X'] = fe.index * 2 / 10 + 1
    fe['deltaG'] = df['dA'] / df['dA'].max()

    sns.scatterplot(data=fe, x='X', y='deltaG', hue='hue', palette=sat_colors)

    ymin = fe['deltaG'].min() // 1 - 1
    yticks = [-2.5 * x for x in range(int(ymin/2.5) + 1)]

    ax.set_xticks(ticks=fe['X'], labels=names, fontsize=10)
    ax.set_yticks(ticks=yticks, fontsize=10)
    ax.set_ylabel('\u0394\u0394G \n (kcal/mol)', fontsize=10)

    xmax = fe['X'].iloc[-1] + 0.1
    ax.set_xlim(0.9, xmax)
    ax.set_ylim(-ymin, 1, 1)

    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(2)

    plt.tight_layout()
    plt.savefig('ddG_comparison.png', dpi=150)
    return fig

df = compile_all_data(systems, names, _default)
colors = get_colorscheme(n)

paths = plot_paths(df, n, colors)
ddG = plot_ddG(df, colors[::3], names)

for plot in [paths, ddG]:
    plot.show()
