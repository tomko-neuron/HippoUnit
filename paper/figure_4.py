""" Produces Figure 4 from Tomko, Benuskova, Jedlicka (2021):
A new reduced-morphology model for CA1 pyramidal cells
and its validation and comparison with other models using HippoUnit """

# _title_   : figure_4.py
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
path_save = './figs/figure_4/'
path_data = './data/'
labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18']
colors_fig = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson']
plt.rc('font', family='sans-serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')


def main():
    fig_4a()
    fig_4b()
    fig_4c()
    legend()


def legend():
    labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18', 'exp_strong_prop', 'exp_weak_prop']
    colors = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson', 'lightcoral']
    handles = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(7)]
    fig = plt.figure(figsize=(8.27, 4))
    plt.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=7)
    plt.gca().set_axis_off()
    plt.savefig(path_save + 'legend' + '.svg', format='svg', bbox_inches='tight')
    plt.savefig(path_save + 'legend' + '.png', format='png', bbox_inches='tight')


def fig_4a():
    fig, ax = plt.subplots(nrows=5, ncols=2, figsize=(4.5, 11.69))

    objects = pickle.load(gzip.GzipFile(
        '../validation_results/temp_data/backpropagating_AP/Cutsuridis_CA1_2010/cclamp_0.09.p', 'rb'))
    ap_prox = objects['v_rec'][50][('PyramidalCell[0].radTprox', 0.5)]
    ap_dist = objects['v_rec'][350][('PyramidalCell[0].radTdist', 0.7857142857142856)]
    ax[0][0].plot(objects['T'], ap_prox, label='prox_50', color='tomato')
    ax[0][0].plot(objects['T'], ap_dist, label='dist_350', color='salmon')
    ax[0][0].set_ylabel('AP1_amp (mV)')
    ax[0][0].set_xlabel('Time (ms)')
    ax[0][0].set_xlim(512, 523)
    ax[0][0].set_ylim(-80, 45)
    ax[0][0].legend(loc='upper right')

    ax[0][1].plot(objects['T'], ap_prox, label='prox_50', color='tomato')
    ax[0][1].plot(objects['T'], ap_dist, label='dist_350', color='salmon')
    ax[0][1].set_ylabel('AP_last_amp (mV)')
    ax[0][1].set_xlabel('Time (ms)')
    ax[0][1].set_xlim(1477, 1488)
    ax[0][1].set_ylim(-80, 45)
    ax[0][1].legend(loc='upper right')

    objects = pickle.load(gzip.GzipFile(
        '../validation_results/temp_data/backpropagating_AP/'
        'Cutsuridis_Poirazi_CA1_2015/cclamp_1.0.p', 'rb'))
    ap_prox = objects['v_rec'][50][('CA1PyramidalCell[0].radTprox', 0.5)]
    ap_dist = objects['v_rec'][340][('CA1PyramidalCell[0].radTdist', 0.7)]
    ax[1][0].plot(objects['T'], ap_prox, label='prox_50', color='goldenrod')
    ax[1][0].plot(objects['T'], ap_dist, label='dist_350', color='gold')
    ax[1][0].set_ylabel('AP1_amp (mV)')
    ax[1][0].set_xlabel('Time (ms)')
    ax[1][0].set_xlim(498, 509)
    ax[1][0].set_ylim(-80, 45)
    ax[1][0].legend(loc='upper right')

    ax[1][1].plot(objects['T'], ap_prox, label='prox_50', color='goldenrod')
    ax[1][1].plot(objects['T'], ap_dist, label='dist_350', color='gold')
    ax[1][1].set_ylabel('AP_last_amp (mV)')
    ax[1][1].set_xlabel('Time (ms)')
    ax[1][1].set_xlim(1486, 1497)
    ax[1][1].set_ylim(-80, 45)
    ax[1][1].legend(loc='upper right')

    objects = pickle.load(gzip.GzipFile(
        '../validation_results/temp_data/backpropagating_AP/'
        'Turi_CA1_2019/cclamp_0.14250000000000004.p', 'rb'))
    ap_prox = objects['v_rec'][50][('PyramidalCell[0].radTprox', 0.5)]
    ap_dist = objects['v_rec'][350][('PyramidalCell[0].radTdist', 0.7857142857142856)]
    ax[2][0].plot(objects['T'], ap_prox, label='prox_50', color='forestgreen')
    ax[2][0].plot(objects['T'], ap_dist, label='dist_350', color='limegreen')
    ax[2][0].set_ylabel('AP1_amp (mV)')
    ax[2][0].set_xlabel('Time (ms)')
    ax[2][0].set_xlim(512, 523)
    ax[2][0].set_ylim(-80, 45)
    ax[2][0].legend(loc='upper right')

    ax[2][1].plot(objects['T'], ap_prox, label='prox_50', color='forestgreen')
    ax[2][1].plot(objects['T'], ap_dist, label='dist_350', color='limegreen')
    ax[2][1].set_xlabel('Time (ms)')
    ax[2][1].set_ylabel('AP_last_amp (mV)')
    ax[2][1].set_xlim(1434, 1445)
    ax[2][1].set_ylim(-80, 45)
    ax[2][1].legend()

    objects = pickle.load(gzip.GzipFile(
        '../validation_results/temp_data/backpropagating_AP/'
        'Tomko_CA1_v2_weak/cclamp_0.8.p', 'rb'))
    ap_prox = objects['v_rec'][50][('CA1_PC_Tomko[0].radTprox', 0.5)]
    ap_dist = objects['v_rec'][350][('CA1_PC_Tomko[0].radTdist', 0.7727272727272728)]
    ax[3][0].plot(objects['T'], ap_prox, label='prox_50', color='darkorchid')
    ax[3][0].plot(objects['T'], ap_dist, label='dist_350', color='orchid')
    ax[3][0].set_ylabel('AP1_amp (mV)')
    ax[3][0].set_xlabel('Time (ms)')
    ax[3][0].set_xlim(502, 513)
    ax[3][0].set_ylim(-80, 45)
    ax[3][0].legend(loc='upper right')

    ax[3][1].plot(objects['T'], ap_prox, label='prox_50', color='darkorchid')
    ax[3][1].plot(objects['T'], ap_dist, label='dist_350', color='orchid')
    ax[3][1].set_xlabel('Time (ms)')
    ax[3][1].set_ylabel('AP_last_amp (mV)')
    ax[3][1].set_xlim(1496, 1507)
    ax[3][1].set_ylim(-80, 45)
    ax[3][1].legend(loc='upper right')

    objects = pickle.load(gzip.GzipFile(
        '../validation_results/temp_data/backpropagating_AP/'
        'Migliore_CA1_pyr_08/cclamp_0.5.p', 'rb'))
    ap_prox = objects['v_rec'][50][('CA1_PC_cAC_sig6[0].apic[0]', 0.5)]
    ap_dist = objects['v_rec'][350][('CA1_PC_cAC_sig6[0].apic[31]', 0.5)]
    ax[4][0].plot(objects['T'], ap_prox, label='prox_50', color='navy')
    ax[4][0].plot(objects['T'], ap_dist, label='dist_350', color='mediumblue')
    ax[4][0].set_ylabel('AP1_amp (mV)')
    ax[4][0].set_xlabel('Time (ms)')
    ax[4][0].set_xlim(505, 516)
    ax[4][0].set_ylim(-80, 45)
    ax[4][0].legend(loc='upper right')

    ax[4][1].plot(objects['T'], ap_prox, label='prox_50', color='navy')
    ax[4][1].plot(objects['T'], ap_dist, label='dist_350', color='mediumblue')
    ax[4][1].set_xlabel('Time (ms)')
    ax[4][1].set_ylabel('AP_last_amp (mV)')
    ax[4][1].set_xlim(1476, 1487)
    ax[4][1].set_ylim(-80, 45)
    ax[4][1].legend(loc='upper right')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_4a' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_4a' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_4b():
    data = json.load(
        open(path_data + 'bAP_amps_all.json'))

    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(3.77, 5))
    i = 0
    for l in labels:
        amps = []
        dists = []
        if len(data[l].keys()) > 0:
            for key in data[l].keys():
                amps.append(data[l][key]['AP1_amp'])
                dists.append(data[l][key]['actual_distance'])
            ax[0].plot(dists, amps, label=l, marker='o', linestyle='none', color=colors_fig[i], zorder=(i + 1) * 2)
        i = i + 1

    dists_exp = [50, 150, 250]
    amps = []
    errs = []
    for d in dists_exp:
        amps.append(data['exp'][str(d)]['AP1_amp'])
        errs.append(data['exp'][str(d)]['AP1_amp_std'] * 2)
    ax[0].errorbar(dists_exp, amps, yerr=errs, marker='o', linestyle='none', color=colors_fig[-1], zorder=(i + 1) * 2)
    ax[0].errorbar(350, data['exp']['350']['AP1_weak_amp'],
                   yerr=data['exp']['350']['AP1_weak_amp_std'] * 2,
                   marker='o', linestyle='none', color="lightcoral", zorder=(i + 1) * 2)
    ax[0].errorbar(350, data['exp']['350']['AP1_strong_amp'],
                   yerr=data['exp']['350']['AP1_strong_amp_std'] * 2,
                   marker='o', linestyle='none', color=colors_fig[-1], zorder=(i + 1) * 2)
    ax[0].set_ylim((0, 100))
    ax[0].set_ylabel('AP1_amp (mV)')
    ax[0].set_xlabel('Distance from soma (um)')

    i = 0
    for l in labels:
        amps = []
        dists = []
        if len(data[l].keys()) > 0:
            for key in data[l].keys():
                amps.append(data[l][key]['APlast_amp'])
                dists.append(data[l][key]['actual_distance'])
            ax[1].plot(dists, amps, label=l, marker='o', linestyle='none', color=colors_fig[i], zorder=(i + 1) * 2)
        i = i + 1

    dists_exp = [50, 150, 250, 350]
    amps = []
    errs = []
    vals_up = []
    vals_down = []
    for d in dists_exp:
        amps.append(data["exp"][str(d)]['APlast_amp'])
        errs.append(data["exp"][str(d)]['APlast_amp_std'] * 2)
        vals_up.append(data["exp"][str(d)]['APlast_amp'] + data['exp'][str(d)]['APlast_amp_std'] * 2)
        vals_down.append(data["exp"][str(d)]['APlast_amp'] - data['exp'][str(d)]['APlast_amp_std'] * 2)
    ax[1].errorbar(dists_exp, amps, yerr=errs, marker='o', linestyle='none', color=colors_fig[-1], zorder=(i + 1) * 2)
    ax[1].plot(dists_exp, vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[1].plot(dists_exp, vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
    ax[1].fill_between(dists_exp, vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)
    ax[1].set_ylabel('APlast_amp (mV)')
    ax[1].set_xlabel('Distance from soma (um)')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_4b' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_4b' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_4c():
    data = json.load(
        open(path_data + 'bAP_errors_all.json'))

    xticks_pos = np.arange(0, 9, 1)
    xticks = ['50_AP1_error', '50_APlast_error', '150_AP1_error', '150_APlast_error', '250_AP1_error',
              '250_APlast_error', '350_AP1_strong_error', '350_AP1_weak_error', '350_APlast_error']

    dists = ['50', '150', '250', '350']
    bar_width = 1.0 / (len(labels) + 1)
    i = 0

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.77, 4))
    for l in labels:
        errs = []
        for d in dists:
            if d != '350':
                errs.append(data[l][d]['AP1_error'])
                errs.append(data[l][d]['APlast_error'])
            else:
                errs.append(data[l][d]['AP1_strong_error'])
                errs.append(data[l][d]['AP1_weak_error'])
                errs.append(data[l][d]['APlast_error'])
        r = [x + i * bar_width for x in np.arange(len(xticks_pos))]
        plt.bar(r, errs, width=bar_width, edgecolor='white', label=labels[i], color=colors_fig[i], zorder=0)
        i = i + 1

    plt.hlines(2, -0.2, 9.2, color=colors_fig[-1], zorder=2)
    plt.xlim(-0.2, 9.2)
    plt.xticks([r + bar_width * 2 for r in range(len(xticks))], xticks, rotation=90)
    plt.ylabel('Error (# std)')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_4c' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_4c' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
