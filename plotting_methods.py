#!/usr/bin/env python
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle

def compile_all_data(systems, names, _default):
    if _default:
        dest = 'run/ParseFEP.log'
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

    ord_df = dframe[dframe['direction'] == 'free_energy'].loc[:,['dA', 'system']]
    order = ord_df.sort_values(by='dA').loc[:, 'system']
    hue_order = np.array([[f'{o}-{direction}' 
                    for direction in ['forward', 'backward', 'free_energy']] 
                    for o in order]).flatten()

    g = sns.lineplot(data=dframe, x='lambda', y='dA', hue='hue', hue_order=hue_order,
                    style=style, ax=ax, palette=colors)
    
    ax.set_xlabel('\u03BB', fontsize=20)
    ax.set_ylabel('\u0394G$_{unbinding}$ (kcal/mol)', fontsize=20)

    ymin = ((dframe['dA'].min() // 10) - 1) * 10
    ymax = ((dframe['dA'].max() // 10) + 1) * 10
    ax.set_ylim(ymin, ymax)
    
    h, l = ax.get_legend_handles_labels()
    labels = []
    for label in l[:-3]:
        if 'free_energy' in label:
            lab = f'{label.split("-")[0]} \u0394G = '
            lab += f'{dframe.loc[dframe["hue"] == label, "dA"].values[0]:.2f} kcal/mol'
        else:
            lab = ' '.join([x for x in label.split('-')])

        labels.append(lab)
    
    for i in range(len(h)//3 - 1):
        h[i*3 + 2] = Rectangle((0,0), 1, 1, fill=False, edgecolor='none', visible=False)

    lgd = plt.legend(h[:-3], labels, bbox_to_anchor=(1, 1.05), 
                 prop={'size': 12}, fancybox=True)
    frame = lgd.get_frame()
    frame.set_facecolor('xkcd:light grey')

    plt.savefig('dG_lambda_forw_back.png', dpi=150, 
                bbox_extra_artists=(lgd,), bbox_inches='tight')


def plot_ddG(df, n, names, sat_colors):
    fig = plt.figure(figsize=(n+2, n))
    spec = gridspec.GridSpec(ncols=n+1, nrows=1, figure=fig)
    ax1 = fig.add_subplot(spec[0, :n])
    ax2 = fig.add_subplot(spec[0, n])

    fe = df.loc[df['direction'] == 'free_energy', 'dA':'system'].reset_index(drop=True)
    fe['deltaG'] = fe['dA'] - fe['dA'].min()
    fe.loc[fe['deltaG'] != 0., 'deltaG'] *= -1
    fe = fe.sort_values(by='deltaG', ascending=False).reset_index(drop=True)
    fe['X'] = fe.index * 2 / 10 + 1

    sns.scatterplot(data=fe, x='X', y='deltaG', hue='system', 
                        palette=sat_colors, ax=ax1)

    ymin = fe['deltaG'].min() // 1 - 1
    yticks = [-2.5 * x for x in range(int(ymin/2.5) + 1)]
    
    ax1.set_xticks(ticks=fe['X'], labels=names, 
                    rotation=45, fontsize=10)
    ax1.set_yticks(ticks=yticks, fontsize=10)
    ax1.set_ylabel('\u0394\u0394G \n (kcal/mol)', fontsize=10)
    ax1.set_xlabel('')

    h, l = ax1.get_legend_handles_labels()
    l = [f'{en:.2f} kcal/mol' for en in fe['deltaG']]
    ax1.get_legend().remove()
    lgd = ax2.legend(h, l, title='Rel. Binding Free Energy', fancybox=True,
                    loc='upper left', bbox_to_anchor=(-0.05,1.))
    ax2.axis('off')

    xmax = fe['X'].iloc[-1] + 0.1
    ax1.set_xlim(0.9, xmax)
    ax1.set_ylim(ymin, 1)

    sns.despine(trim=True)

    plt.tight_layout()
    plt.savefig('ddG_comparison.png', dpi=150, bbox_extra_artists=(lgd,), bbox_inches='tight')
