""" Produces Figure 2 from Tomko, Benuskova, Jedlicka (2021):
A new reduced-morphology model for CA1 pyramidal cells
and its validation and comparison with other models using HippoUnit """

# _title_   : figure_2.py
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
path_save = './figs/figure_2/'
path_data = './data/'
labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18']
colors_fig = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson']
plt.rc('font', family='sans-serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')


def main():
    fig_2a()
    fig_2b()
    legend()


def legend():
    labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18', 'exp']
    colors = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson']
    handles = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(6)]
    fig = plt.figure(figsize=(8.27, 4))
    plt.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=6)
    plt.gca().set_axis_off()
    plt.savefig(path_save + 'legend' + '.svg', format='svg', bbox_inches='tight')
    plt.savefig(path_save + 'legend' + '.png', format='png', bbox_inches='tight')


def fig_2a():
    path = '../validation_results/temp_data/depol_block/'
    files = ['Cutsuridis_CA1_2010/cclamp_1.6.p', 'Cutsuridis_Poirazi_CA1_2015/cclamp_1.6.p',
             'Turi_CA1_2019/cclamp_1.6.p',
             'Tomko_CA1_v2_weak/cclamp_1.25.p', 'Migliore_CA1_pyr_08/cclamp_1.4000000000000001.p']
    amps = ['1.6 nA', '1.6 nA', '1.6 nA', '1.25 nA', '1.4 nA']

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(8.27, 4.5), constrained_layout=True)
    obj = pickle.load(gzip.GzipFile(path + files[0], 'rb'))
    v_vec = obj[0]['V']
    t_vec = obj[0]['T']
    ax[0][0].plot(t_vec, v_vec, color=colors_fig[0], label=amps[0])
    ax[0][0].set_ylim(-80, 40)
    ax[0][0].set_xlabel('Time (ms)')
    ax[0][0].set_ylabel('Voltage (mV)')
    ax[0][0].set_title(labels[0])
    ax[0][0].legend(loc='upper right')

    obj = pickle.load(gzip.GzipFile(path + files[1], 'rb'))
    v_vec = obj[0]['V']
    t_vec = obj[0]['T']
    ax[0][1].plot(t_vec, v_vec, color=colors_fig[1], label=amps[1])
    ax[0][1].set_ylim(-80, 40)
    ax[0][1].set_xlabel('Time (ms)')
    ax[0][1].set_title(labels[1])
    ax[0][1].legend(loc='upper right')

    obj = pickle.load(gzip.GzipFile(path + files[2], 'rb'))
    v_vec = obj[0]['V']
    t_vec = obj[0]['T']
    ax[0][2].plot(t_vec, v_vec, color=colors_fig[2], label=amps[2])
    ax[0][2].set_ylim(-80, 40)
    ax[0][2].set_xlabel('Time (ms)')
    ax[0][2].set_title(labels[2])
    ax[0][2].legend(loc='upper right')

    obj = pickle.load(gzip.GzipFile(path + files[3], 'rb'))
    v_vec = obj[0]['V']
    t_vec = obj[0]['T']
    ax[1][0].plot(t_vec, v_vec, color=colors_fig[3], label=amps[3])
    ax[1][0].set_ylim(-80, 40)
    ax[1][0].set_xlabel('Time (ms)')
    ax[1][0].set_ylabel('Voltage (mV)')
    ax[1][0].set_title(labels[3])
    ax[1][0].legend(loc='upper right')

    obj = pickle.load(gzip.GzipFile(path + files[4], 'rb'))
    v_vec = obj[0]['V']
    t_vec = obj[0]['T']
    ax[1][1].plot(t_vec, v_vec, color=colors_fig[4], label=amps[4])
    ax[1][1].set_ylim(-80, 40)
    ax[1][1].set_xlabel('Time (ms)')
    ax[1][1].set_title(labels[4])
    ax[1][1].legend(loc='upper right')

    ax[1][2].axis('off')
    plt.savefig(path_save + 'fig_2a' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_2a' + '.svg', format='svg', bbox_inches='tight')


def fig_2b():
    data = json.load(
        open(path_data + 'depol_block_all.json'))
    r = np.arange(0, 3, 1)
    labels_depol = ['To21', 'M18', 'exp']

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8.27, 2.25))
    ax[0].plot(0, data['To21']['Veq'], marker='o', linestyle='none', label=labels[3], color=colors_fig[3], zorder=2)
    ax[0].plot(1, data['M18']['Veq'], marker='o', linestyle='none', label=labels[4], color=colors_fig[4], zorder=2)
    ax[0].errorbar(2, data['experiment']['mean_Veq'],
                   yerr=2 * data['experiment']['Veq_std'], label='exp',
                   marker='o', linestyle='none', color=colors_fig[-1], zorder=4)
    vals_up = np.full(2, data['experiment']['mean_Veq'] + 2 * data['experiment']['Veq_std'])
    vals_down = np.full(2, data['experiment']['mean_Veq'] - 2 * data['experiment']['Veq_std'])
    ax[0].plot([-0.2, 2.2], vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[0].plot([-0.2, 2.2], vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[0].fill_between([-0.2, 2.2], vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)
    ax[0].set_xticks(r)
    ax[0].set_xticklabels(labels_depol)
    ax[0].set_xlim(-0.2, 2.2)
    ax[0].set_ylim(-47.0, 1.0)
    ax[0].set_ylabel('Veq (mV)')

    ax[1].plot(0, data['To21']['I_below_depol_block'], marker='o', linestyle='none', label=labels[3],
               color=colors_fig[3], zorder=2)
    ax[1].plot(1, data['M18']['I_below_depol_block'], marker='o', linestyle='none', label=labels[4],
               color=colors_fig[4], zorder=2)
    ax[1].errorbar(2, data['experiment']['mean_Ith'],
                   yerr=2 * data['experiment']['Ith_std'], label='exp',
                   marker='o', linestyle='none', color=colors_fig[-1], zorder=4)
    vals_up = np.full(2, data['experiment']['mean_Ith'] + 2 * data['experiment']['Ith_std'])
    vals_down = np.full(2, data['experiment']['mean_Ith'] - 2 * data['experiment']['Ith_std'])
    ax[1].plot([-0.2, 2.2], vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[1].plot([-0.2, 2.2], vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[1].fill_between([-0.2, 2.2], vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)
    ax[1].set_xticks(r)
    ax[1].set_xticklabels(labels_depol)
    ax[1].set_xlim(-0.2, 2.2)
    ax[1].set_ylabel('I_below_depol_block (nA)')

    data = json.load(
        open(path_data + 'depol_block_errors_all.json'))
    ax[2].plot(1 / 3, data['To21']['Veq_error'], marker='o', linestyle='none', label=labels[3],
               color=colors_fig[3], zorder=0)
    ax[2].plot(2 / 3, data['To21']['Ith_error'], marker='o', linestyle='none', color=colors_fig[3], zorder=0)
    ax[2].plot(1 / 3, data['M18']['Veq_error'], marker='o', linestyle='none', label=labels[4],
               color=colors_fig[4], zorder=0)
    ax[2].plot(2 / 3, data['M18']['Ith_error'], marker='o', linestyle='none', color=colors_fig[4], zorder=0)
    ax[2].set_xticks([1 / 3, 2 / 3])
    ax[2].set_xticklabels(['Veq_error', 'Ith_error'], rotation=45)
    ax[2].set_ylabel('Error (# std)')
    ax[2].hlines(2, 0, 1, color=colors_fig[-1], zorder=2)
    ax[2].set_xlim(0, 1)
    ax[2].set_ylim(0.0, 2.6)

    fig.tight_layout()
    plt.savefig(path_save + 'fig_2b' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_2b' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
