""" Produces Figure 3 from Tomko, Benuskova, Jedlicka (2021):
A new reduced-morphology model for CA1 pyramidal cells
and its validation and comparison with other models using HippoUnit """

# _title_   : figure_3.py
# _author_  : Matus Tomko
# _mail_    : matus.tomko __at__ fmph.uniba.sk

import json
import matplotlib
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt

matplotlib.use('Agg')
path_save = './figs/figure_3/'
path_data = './data/'
labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18']
labels_exp = ['C10', 'CP15', 'Tu19', 'To21', 'M18', 'exp']
colors_fig = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson']
plt.rc('font', family='sans-serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')


def main():
    handles = [mpatches.Patch(color=colors_fig[i], label=labels_exp[i]) for i in range(6)]
    fig = plt.figure(figsize=(8.27, 4))
    plt.legend(handles, labels_exp, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=6)
    plt.gca().set_axis_off()
    plt.savefig(path_save + 'legend' + '.svg', format='svg', bbox_inches='tight')
    plt.savefig(path_save + 'legend' + '.png', format='png', bbox_inches='tight')

    data = json.load(
        open(path_data + 'PSP_attenuation_all.json'))
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8.27, 3))
    for i in range(len(labels)):
        dists = []
        vals = []
        for key, value in data[labels[i]].items():
            dists.append(value['distance'])
            vals.append(value['attenuation_soma/dendrite'])
        ax[0].plot(dists, vals, label=labels[i], marker='o', linestyle='none', color=colors_fig[i], zorder=(i + 1) * 2)

    dists = []
    vals = []
    dist_l = ['dist_100', 'dist_200', 'dist_300']
    errs = []
    vals_up = []
    vals_down = []
    for d in dist_l:
        dists.append(data['exp'][d]['distance'])
        vals.append(data['exp'][d]['attenuation_soma/dendrite'])
        errs.append(data['exp'][d]['attenuation_soma/dendrite_std'] * 2)
        vals_up.append(
            data['exp'][d]['attenuation_soma/dendrite'] + 2 * data['exp'][d]['attenuation_soma/dendrite_std'])
        vals_down.append(
            data['exp'][d]['attenuation_soma/dendrite'] - 2 * data['exp'][d]['attenuation_soma/dendrite_std'])
    ax[0].errorbar(dists, vals,
                   yerr=errs, label='exp',
                   marker='o', linestyle='none', color=colors_fig[-1], zorder=(len(labels) + 1) * 2)
    ax[0].plot(dists, vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[0].plot(dists, vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[0].fill_between(dists, vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)
    ax[0].set_xlabel('Distance from soma (um)')
    ax[0].set_ylabel('Attenuation soma / dendrite')

    data = json.load(
        open(path_data + 'PSP_attenuation_errors_all.json'))
    bar_width = 0.16
    i = 0

    for l in labels:
        r = [x + i * bar_width for x in np.arange(3)]
        errs = []
        errs.append(data[l]['error_attenuation_soma/dend_100_um'])
        errs.append(data[l]['error_attenuation_soma/dend_200_um'])
        errs.append(data[l]['error_attenuation_soma/dend_300_um'])
        ax[1].bar(r, errs, width=bar_width, edgecolor='white', label=l, color=colors_fig[i], zorder=0)
        i = i + 1
    ax[1].set_xlabel('Distance from the soma (um)')
    ax[1].set_ylabel('Error (# std)')
    ax[1].hlines(2, -0.28, 2.92, color=colors_fig[-1], zorder=2)
    ax[1].set_xlim(-0.28, 2.92)
    ax[1].set_xticks([r + bar_width * 2 for r in range(3)])
    ax[1].set_xticklabels(['100', '200', '300'])

    fig.tight_layout()
    plt.savefig(path_save + 'fig_3a' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_3a' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
