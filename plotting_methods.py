#!/usr/bin/env python
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle
from matplotlib import rc

rc('axes', linewidth=1.5)
rc('font', weight='bold')
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

def compile_all_data(systems, names, _default):
    if _default:
        dest = 'run/ParseFEP.log'
    else:
        dest = 'ParseFEP.log'

    df = pd.DataFrame()
    for (system, name) in zip(systems, names):
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
    
    dframe = pd.DataFrame(data, columns=['direction', 'lambda', 'ddA', 'dA', 'dSig'], dtype=float)
    
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
    
    # reverse lambda direction and subtract `dA` values by overall delta G. This is done
    # to obtain the paths for binding rather than unbinding (simply the reverse of what we
    # have simulated)
    dframe['lambda'] = 1. - dframe['lambda']

    fes = dframe[dframe['direction'] == 'free_energy']
    for sys in fes['system']:
        slc = dframe[(dframe['system'] == sys) & (dframe['direction'] != 'free_energy')]
        slc['dA'] = slc['dA'] - dframe[(dframe['system'] == sys) & (dframe['direction'] == 'free_energy')].loc[:,'dA'].iloc[0]
        dframe[(dframe['system'] == sys) & (dframe['direction'] != 'free_energy')] = slc

    g = sns.lineplot(data=dframe, x='lambda', y='dA', hue='hue', hue_order=hue_order,
                    style=style, ax=ax, palette=colors)
    
    ax.set_xlabel('\u03BB', fontsize=20)
    ax.set_ylabel('\u0394G$_{binding}$ (kcal/mol)', fontsize=20)

    ymin = ((dframe['dA'].min() // 10) - 1) * 10
    ymax = ((dframe['dA'].max() // 10) + 1) * 10
    ax.set_ylim(ymin, ymax)
    
    h, l = ax.get_legend_handles_labels()
    labels = []
    for label in l[:-3]:
        if 'free_energy' in label:
            lab = f'{label.split("-")[0]} \u0394G = '
            lab += f'-{dframe.loc[dframe["hue"] == label, "dA"].values[0]:.2f} kcal/mol'
        else:
            lab = ' '.join([x for x in label.split('-')])

        labels.append(lab)
    
    for i in range(len(h)//3 - 1):
        h[i*3 + 2] = Rectangle((0,0), 1, 1, fill=False, edgecolor='none', visible=False)

    lgd = plt.legend(h[:-3], labels, bbox_to_anchor=(1, 1.05), 
                 prop={'size': 12}, fancybox=True)
    frame = lgd.get_frame()
    frame.set_facecolor('xkcd:light grey')

    plt.savefig('dG_lambda_forw_back.png', dpi=250, 
                bbox_extra_artists=(lgd,), bbox_inches='tight')


def plot_ddG(df, n, names, sat_colors):
    size = (2*n, 2*n)
    fig = plt.figure(figsize=size)
    spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
    ax1 = fig.add_subplot(spec[0, :])

    fe = df.loc[df['direction'] == 'free_energy', 'dA':'system'].reset_index(drop=True)
    fe['deltaG'] = fe['dA'] - fe['dA'].min()
    fe.loc[fe['deltaG'] != 0., 'deltaG'] *= -1
    fe = fe.sort_values(by='deltaG', ascending=False).reset_index(drop=True)
    fe['X'] = fe.index * 2 / 10 + 1

    sns.scatterplot(data=fe, x='X', y='deltaG', hue='system', 
                        palette=sat_colors, ax=ax1, legend=False)
    
    ymin = fe['deltaG'].min() // 1 - 1
    yticks = [-2.5 * x for x in range(int(ymin/2.5) + 1)]
    
    ax1.set_xticks(ticks=fe['X'], labels=names, 
                    rotation=45, fontsize=10)
    ax1.set_yticks(ticks=yticks, fontsize=10)
    ax1.set_ylabel('\u0394\u0394G \n (kcal/mol)', fontsize=10)
    ax1.set_xlabel('')
    ax1.set_title('Binding Free Energy Difference(s)', fontsize=15)

    xmax = fe['X'].iloc[-1] + 0.1
    ax1.set_xlim(0.9, xmax)
    ax1.set_ylim(ymin, 1)

    sns.despine(trim=True)

    x = np.linspace(fe['X'][0], fe['X'][n-1], 50)
    dash1, = ax1.plot(x, [0]*50, color='black')
    dash1.set_dashes([2, 2, 10, 2])
    ax1.text((fe['X'][n-1] - 1)/2 + 1., 0.2, '0 kcal/mol', horizontalalignment='center')

    for k in range(1, n):
        y_k = fe['deltaG'][k]
        y = np.linspace(0, y_k, 50)
        dash, = ax1.plot([fe['X'][k]]*50, y, color='black')
        dash.set_dashes([4,4])
        ax1.text(fe['X'][k]+0.01, y_k/2, f'{fe["deltaG"][k]:.2f} kcal/mol',
                    rotation=90, verticalalignment='center')

    plt.tight_layout()
    plt.savefig('ddG_comparison.png', dpi=250)
