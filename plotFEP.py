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

args = parser.parse_args()
filepath = args.filepath
names = args.systems.split(' ')
systems = [os.join(filepath, system) for system in names]
n = len(systems)

assert n < 11, f'ERROR: colormap only contains 10 color combinations \
                    but you provided {n} systems!'

def compile_all_data(systems, names):
    df = pd.DataFrame()
    for i, (system, name) in enumerate(zip(systems, names)):
        temp = extract_data(f'{system}/run/results/ParseFEP.log')
        temp['system'] = name
        df = pd.concat([df, temp])
    
    df['hue'] = df['system'] + '-' + df['direction']
    return df


def extract_data(logfile):
    lines = [line.strip() for line in open(logfile).readlines() if ':' in line]
    data = [line.split() for line in lines[:102]]
    bar = lines[-1].split()
    data.append(['free_energy', '1', '0', bar[6], bar[-1]])
    
    dframe = pd.DataFrame(data, columns=['direction', 'lambda', 'ddA', 'dA', 'dSig'])
    dframe['direction'] = df['direction'].str[:-1]
    dframe.loc['lambda':'dSig'] = dframe.loc['lambda':'dSig'].astype(float)

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
    colorscheme[2::3] = [' '] * n

    return colorscheme


def plot_paths(dframe, n, colors):
    fig, ax = plt.subplots(1,1, figsize=(5,5))
    style = ['-', '--', ''] * n
    
    sns.lineplot(data=dframe, x='lambda', y='dA', hue='hue', style='hue',
                    ax=ax, palette=colors, style_order=style)
    
    ax.set_xlabel('\u03BB', fontsize=20)
    ax.set_ylabel('\u0394G$_{binding}$ (kcal/mol)', fontsize=20)

    ymin = ((df['dA'].min() // 10) - 1) * 10
    ymax = ((df['dA'].max() // 10) + 1) * 10
    ax.set_ylim(ymin, ymax)
    
    legend = plt.legend(bbox_to_anchor=(1, 1.05), prop={'size': 12})
    frame = legend.get_frame()
    frame.set_facecolor('xkcd:light grey')

    plt.savefig('dG_lambda_forw/back.png', dpi=150)
    return fig


def plot_ddG(df, sat_colors):
    fig, ax = plt.subplots(1,1, figsize=(2,2))

    fe = df[df'direction'] == 'free_energy'].reset_index(drop=True)
    fe['X'] = fe.index * 2 / 10 + 1
    fe['deltaG'] = df['dA'] / df['dA'].max()

    sns.scatterplot(data=df_fe, x='X', y='deltaG', hue='hue', palette=sat_colors)

    ax.set_xticks(ticks=X, labels=, fontsize=10)
    ax.set_yticks(ticks=, labels=, fontsize=10)
    ax.set_label('\u0394\u0394G \n (kcal/mol)', fontsize=10)

    xmax = X[-1] + 0.1
    ymin = (min(delta_G) // 1) - 1
    ax.set_xlim(0.9, xmax)
    ax.set_ylim(-ymin, 1, 1)

    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(2)

    plt.savefig('ddG_comparison.png', dpi=150)
    return fig


df = compile_all_data(systems, names)
colors = get_colorscheme(n)

paths = plot_paths(df, n, colors)
ddG = plot_ddG(df, colors[::3])

for plot in [paths, ddG]:
    plot.show()
