""" Produces Figure 1 from Tomko, Benuskova, Jedlicka (2021):
A new reduced-morphology model for CA1 pyramidal cells
and its validation and comparison with other models using HippoUnit """

# _title_   : figure_1.py
# _author_  : Matus Tomko
# _mail_    : matus.tomko __at__ fmph.uniba.sk

import gzip
import json
import pickle as pickle
import matplotlib
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt

matplotlib.use('Agg')
path_save = './figs/figure_1/'
path_data = './data/'
labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18']
colors_fig = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson']
plt.rc('font', family='sans-serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')


def main():
    legend()
    fig_1a()
    fig_1b()
    fig_1c()
    fig_1d()


def legend():
    labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18', 'exp']
    colors = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson']
    handles = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(6)]
    fig = plt.figure(figsize=(8.27, 4))
    plt.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=6)
    plt.gca().set_axis_off()
    plt.savefig(path_save + 'legend' + '.svg', format='svg', bbox_inches='tight')
    plt.savefig(path_save + 'legend' + '.png', format='png', bbox_inches='tight')


def fig_1a():
    path_traces = '../validation_results/temp_data/somaticfeat_UCL_data/'
    files_traces = ['Cutsuridis_CA1_2010/', 'Cutsuridis_Poirazi_CA1_2015/', 'Turi_CA1_2019/',
                    'Tomko_CA1_v2_weak/', 'Migliore_CA1_pyr_08/']
    files_morphos = ['cutsuridis_PC.png', 'cutsuridis_poirazi_PC.png', 'turi_PC.png',
                     'tomko_PC.png', 'migliore_PC.png']
    step_pos = 'Step0.6'
    step_neg = 'Step-0.6'

    fig, ax = plt.subplots(nrows=3, ncols=5, figsize=(8.27, 6))

    i = 0
    for file in files_morphos:
        img = plt.imread(path_save + file)
        ax[0][i].imshow(img)
        ax[0][i].set_title(labels[i])
        ax[0][i].tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
        i = i + 1

    i = 0
    for file in files_traces:
        obj = pickle.load(gzip.GzipFile(path_traces + file + step_pos + '.p', 'rb'))
        t_vec = obj[step_pos][0]
        v_vec = obj[step_pos][1]
        ax[1][i].plot(t_vec, v_vec, color=colors_fig[i], label='0.6 nA')
        ax[1][i].set_ylim(-80, 80)
        ax[1][i].yaxis.set_ticks(np.arange(-80, 80, 20))
        ax[1][i].set_xlim(950, 1450)
        ax[1][i].legend(loc='upper right')
        ax[1][i].set_xlabel('Time (ms)')
        if i == 0:
            ax[1][i].set_ylabel('Voltage (mV)')
        i = i + 1

    i = 0
    for file in files_traces:
        obj = pickle.load(gzip.GzipFile(path_traces + file + step_neg + '.p', 'rb'))
        t_vec = obj[step_neg][0]
        v_vec = obj[step_neg][1]
        ax[2][i].plot(t_vec, v_vec, color=colors_fig[i], label='-0.6 nA')
        ax[2][i].set_ylim(-120, 20)
        ax[2][i].yaxis.set_ticks(np.arange(-120, 20, 20))
        ax[2][i].set_xlim(950, 1450)
        ax[2][i].legend(loc='upper right')
        ax[2][i].set_xlabel('Time (ms)')
        if i == 0:
            ax[2][i].set_ylabel('Voltage (mV)')
        i = i + 1

    fig.tight_layout()
    plt.savefig(path_save + 'fig_1a' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_1a' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_1b():
    data = json.load(
        open(path_data + 'voltage_deflection.json'))
    xticks = ['-1.0', '-0.8', '-0.6', '-0.4', '-0.2']
    r = np.arange(0, 5, 1)
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(2.75, 3))

    for l in range(len(labels)):
        vals = []
        for key, value in data[labels[l]].items():
            vals.append(value['value'])
        ax[0].plot(r, vals, marker='o', linestyle='none', label=labels[l], color=colors_fig[l], zorder=l * 2)

    vals = []
    errs = []
    for key, value in data['experiment'].items():
        vals.append(value['mean'])
        errs.append(value['std'] * 2)
    ax[0].errorbar(r, vals, yerr=errs, label='exp', marker='o', linestyle='none', color=colors_fig[-1],
                   zorder=(len(labels) + 1) * 2)
    ax[0].set_xticks(r)
    ax[0].set_xticklabels(xticks)
    ax[0].set_xlabel('Injected current (nA)')
    ax[0].set_ylabel('Voltage (mV)')
    ax[0].set_ylim(-50.1, 0)

    data = json.load(
        open(path_data + 'voltage_deflection.json'))
    xticks = ['-1.0', '-0.8', '-0.6', '-0.4', '-0.2']
    r = np.arange(0, 5, 1)

    for l in range(len(labels)):
        vals = []
        for key, value in data[labels[l]].items():
            vals.append(value['error'])
        ax[1].plot(r, vals, marker='o', linestyle='none', label=labels[l], color=colors_fig[l])
    ax[1].hlines(2, -0.2, 4.2, color=colors_fig[-1])
    ax[1].set_xlim(-0.2, 4.2)
    ax[1].set_xticks(r)
    ax[1].set_xticklabels(xticks)
    ax[1].set_xlabel('Injected current (nA)')
    ax[1].set_ylabel('Error (# std)')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_1b' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_1b' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_1c():
    amps = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
            0.95, 1., 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6]
    data = json.load(
        open(path_data + 'spike_count.json'))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.51, 3))

    for i in range(len(labels)):
        sp = []
        for a in amps:
            sp.append(data[labels[i]]['Step' + str(a)])
        ax.plot(amps, sp, 'o-', label=labels[i], color=colors_fig[i], zorder=(i + 1) * 2)

    sp = []
    sp_std = []
    vals_up = []
    vals_down = []
    amps = [0.2, 0.4, 0.6, 0.8, 1.0]
    for a in amps:
        sp.append(data['experiment']['Step' + str(a)])
        sp_std.append(data['experiment']['Step' + str(a) + '_std'] * 2)
        vals_up.append(sp[-1] + sp_std[-1])
        if (sp[-1] - sp_std[-1] < 0):
            vals_down.append(0)
        else:
            vals_down.append(sp[-1] - sp_std[-1])
    ax.errorbar(amps, sp,
                yerr=sp_std, label='experiment',
                marker='o', color=colors_fig[-1], zorder=(len(labels) + 2) * 2)
    ax.plot(amps, vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
    ax.plot(amps, vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
    ax.fill_between(amps, vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)
    ax.set_xlabel('Injected current (nA)')
    ax.set_ylabel('Number of APs')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_1c' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_1c' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_1d():
    data = json.load(
        open(path_data + 'spike_event_features_errors.json'))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8.27, 3))
    bar_width = 1.0 / (len(labels) + 1)
    i = 0
    xticks = ['spike_count', 'time_to_last_spike', 'time_to_first_spike', 'inv_time_to_first_spike',
              'inv_first_ISI', 'inv_second_ISI', 'inv_third_ISI', 'inv_fourth_ISI', 'inv_fifth_ISI', 'inv_last_ISI']

    for x in labels:
        err = []
        for y in xticks:
            err.append(data[x][y])
        r = [x + i * bar_width for x in np.arange(len(xticks))]
        ax.bar(r, err, width=bar_width, edgecolor='white', label=labels[i], color=colors_fig[i])
        i = i + 1
    ax.set_ylabel('Error (# std)')
    ax.set_xticks([r + bar_width * 2 for r in range(len(xticks))])
    ax.set_xticklabels(xticks, rotation=45)
    ax.hlines(2, -0.2, 10.2, color=colors_fig[-1])
    ax.set_xlim(-0.2, 10.2)

    fig.tight_layout()
    plt.savefig(path_save + 'fig_1d' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_1d' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
