""" Produces Figures 5-7 from Tomko, Benuskova, Jedlicka (2021):
A new reduced-morphology model for CA1 pyramidal cells
and its validation and comparison with other models using HippoUnit """

# _title_   : figures_5-7.py
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
path_save = 'figs/figures_5-7/'
path_data = './data/'
labels = ['C10', 'CP15', 'Tu19', 'To21', 'M18']
labels_exp = ['C10', 'CP15', 'Tu19', 'To21', 'M18', 'exp']
colors_fig = ['tomato', 'goldenrod', 'forestgreen', 'darkorchid', 'navy', 'crimson']
plt.rc('font', family='sans-serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')


def legend():
    l = ['Tu19', 'To21', 'M18', 'exp']
    colors = ['forestgreen', 'darkorchid', 'navy', 'crimson']
    handles = [mpatches.Patch(color=colors[i], label=l[i]) for i in range(4)]
    fig = plt.figure(figsize=(8.27, 4))
    plt.legend(handles, l, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=4)
    plt.gca().set_axis_off()
    plt.savefig(path_save + 'legend' + '.svg', format='svg', bbox_inches='tight')
    plt.savefig(path_save + 'legend' + '.png', format='png', bbox_inches='tight')


def fig_5a():
    data = json.load(
        open(path_data + 'oblique_integration_all.json'))

    xticks_mean = ['mean_threshold', 'mean_prox_threshold', 'mean_dist_threshold', 'mean_amp_at_th']
    xticks_sd = ['threshold_std', 'prox_threshold_std', 'dist_threshold_std', 'amp_at_th_std']

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3.5))
    for i in range(len(xticks_mean)):
        x = 1
        for l in range(len(labels_exp)):
            if l in [2, 3, 4]:
                if i == 0:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]], label=labels_exp[l],
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                else:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]],
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                x = x + 1
            if l == 5:
                if i == 0:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]] * 2, label=labels_exp[l],
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                else:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]] * 2,
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                x = x + 1
        vals_up = np.full(2, data[labels_exp[-1]][xticks_mean[i]] + 2 * data[labels_exp[-1]][xticks_sd[i]])
        vals_down = np.full(2, data[labels_exp[-1]][xticks_mean[i]] - 2 * data[labels_exp[-1]][xticks_sd[i]])
        plt.plot([i + 0, i + 1], vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
        plt.plot([i + 0, i + 1], vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
        plt.fill_between([i + 0, i + 1], vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)

    plt.xlim(0, 4)
    plt.ylim(0, 12)
    plt.vlines([1, 2, 3], 0, 12, linestyles=[':'], colors='black')
    plt.xticks(np.arange(0.5, 4, 1), ['threshold', 'prox_threshold', 'dist_threshold', 'amplitude_at_th'])
    plt.ylabel('Voltage (mV)')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_5a' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_5a' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_5b():
    data = json.load(
        open(path_data + 'oblique_integration_all.json'))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3.5))

    x = 1
    for l in range(len(labels_exp)):
        if l in [2, 3, 4]:
            plt.errorbar(0.2 * x, data[labels_exp[l]]['mean_time_to_peak'],
                         yerr=data[labels_exp[l]]['time_to_peak_std'], label=labels_exp[l],
                         marker='o', linestyle='none', color=colors_fig[l], zorder=2)
            x = x + 1
        if l == 5:
            plt.errorbar(0.2 * x, data[labels_exp[l]]['mean_time_to_peak'],
                         yerr=2 * data[labels_exp[l]]['time_to_peak_std'], label=labels_exp[l],
                         marker='o', linestyle='none', color=colors_fig[l], zorder=2)
            x = x + 1
    vals_up = np.full(2, data[labels_exp[-1]]['mean_time_to_peak'] + 2 * data[labels_exp[-1]]['time_to_peak_std'])
    vals_down = np.full(2, data[labels_exp[-1]]['mean_time_to_peak'] - 2 * data[labels_exp[-1]]['time_to_peak_std'])
    plt.plot([0, 1], vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
    plt.plot([0, 1], vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
    plt.fill_between([0, 1], vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)
    plt.xlim(0, 1)
    plt.xticks([0.2, 0.4, 0.6, 0.8], ['Tu19', 'To21', 'M18', 'exp'])
    plt.ylabel('Time to peak (ms)')
    plt.ylim(0, 18)

    fig.tight_layout()
    plt.savefig(path_save + 'fig_5b' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_5b' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_5c():
    data = json.load(
        open(path_data + 'oblique_integration_all.json'))
    xticks_mean = ['mean_nonlin_at_th', 'mean_nonlin_suprath', 'mean_async_nonlin']
    xticks_sd = ['nonlin_at_th_std', 'nonlin_suprath_std', 'async_nonlin_std']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3.5))

    for i in range(len(xticks_mean)):
        x = 1
        for l in range(len(labels_exp)):
            if l in [2, 3, 4]:
                if i == 0:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]], label=labels_exp[l],
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                else:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]],
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                x = x + 1
            if l == 5:
                if i == 0:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]] * 2, label=labels_exp[l],
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                else:
                    plt.errorbar(0.2 * x + i, data[labels_exp[l]][xticks_mean[i]],
                                 yerr=data[labels_exp[l]][xticks_sd[i]] * 2,
                                 marker='o', linestyle='none', color=colors_fig[l], zorder=2)
                x = x + 1
        vals_up = np.full(2, data[labels_exp[-1]][xticks_mean[i]] + 2 * data[labels_exp[-1]][xticks_sd[i]])
        vals_down = np.full(2, data[labels_exp[-1]][xticks_mean[i]] - 2 * data[labels_exp[-1]][xticks_sd[i]])
        plt.plot([i + 0, i + 1], vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
        plt.plot([i + 0, i + 1], vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
        plt.fill_between([i + 0, i + 1], vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)

    plt.xlim(0, 3)
    plt.ylim(0, 500)
    plt.vlines([1, 2], 0, 500, linestyles=[':'], colors='black')
    plt.xticks(np.arange(0.5, 3, 1), ['nonlinearity_at_th', 'suprath_nonlinearity', 'asynch_nonlinearity'])
    plt.ylabel('Degree of nonlinearity (%)')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_5c' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_5c' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


def fig_5d():
    data = json.load(
        open(path_data + 'oblique_integration_all.json'))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3.5))

    x = 1
    for l in range(len(labels_exp)):
        if l in [2, 3, 4]:
            plt.errorbar(0.2 * x, data[labels_exp[l]]['mean_peak_deriv'],
                         yerr=data[labels_exp[l]]['peak_deriv_std'], label=labels_exp[l],
                         marker='o', linestyle='none', color=colors_fig[l], zorder=2)
            x = x + 1
        elif l == 5:
            plt.errorbar(0.2 * x, data[labels_exp[l]]['mean_peak_deriv'],
                         yerr=2 * data[labels_exp[l]]['peak_deriv_std'], label=labels_exp[l],
                         marker='o', linestyle='none', color=colors_fig[l], zorder=2)
            x = x + 1
    vals_up = np.full(2, data[labels_exp[-1]]['mean_peak_deriv'] + 2 * data[labels_exp[-1]]['peak_deriv_std'])
    vals_down = np.full(2, data[labels_exp[-1]]['mean_peak_deriv'] - 2 * data[labels_exp[-1]]['peak_deriv_std'])
    plt.plot([0, 1], vals_up, linestyle=':', color=colors_fig[-1], zorder=0)
    plt.plot([0, 1], vals_down, linestyle=':', color=colors_fig[-1], zorder=0)
    plt.fill_between([0, 1], vals_up, vals_down, color=colors_fig[-1], alpha=0.2, zorder=0)
    plt.xlim(0, 1)
    plt.xticks([0.2, 0.4, 0.6, 0.8], ['Tu19', 'To21', 'M18', 'exp'])
    plt.ylabel('Peak dV/dt at threshold (mV/s)')
    plt.ylim(0, 13)

    fig.tight_layout()
    plt.savefig(path_save + 'fig_5d' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_5d' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


# Python 2.7
def fig_5e():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3.5))
    objects = pickle.load(gzip.GzipFile(
        '../validation_results/results/oblique_integration/Turi_CA1_2019/oblique_model_epsp_amps_sync.p', 'rb'))
    plt.plot(objects['all_expected_mean'], objects['all_measured_mean'], 'o-', label=labels[2], color=colors_fig[2],
             zorder=2)
    objects = pickle.load(gzip.GzipFile(
        '../validation_results/results/oblique_integration/Tomko_CA1_v2_weak/oblique_model_epsp_amps_sync.p', 'rb'))
    plt.plot(objects['all_expected_mean'], objects['all_measured_mean'], 'o-', label=labels[3], color=colors_fig[3],
             zorder=4)
    objects = pickle.load(gzip.GzipFile(
        '../validation_results/results/oblique_integration/Migliore_CA1_pyr_08_apic[12]/oblique_model_epsp_amps_sync.p',
        'rb'))
    plt.plot(objects['all_expected_mean'], objects['all_measured_mean'], 'o-', label=labels[4], color=colors_fig[4],
             zorder=6)
    exp_expected = [0, 0.78, 1.8, 2.95, 3.68, 4.84, 5.74, 7.5]
    exp_measured = [0, 0.63, 1.7, 2.86, 4.21, 7.17, 7.96, 9.75]
    plt.plot(exp_expected, exp_measured, 'o-', label=labels_exp[-1], color=colors_fig[-1], zorder=8)
    plt.plot(np.arange(0, 13, 1), np.arange(0, 13, 1), ':', color='black', zorder=0)
    plt.xlim((0, 12))
    plt.ylim((0, 12))
    plt.xlabel('Expected EPSP (mV)')
    plt.ylabel('Measured EPSP (mV)')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_5e' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_5e' + '.svg', format='svg', bbox_inches='tight')
    plt.close()


#Python 2.7
def fig_5f():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3.5))
    inputs = np.arange(0, 11, 1)
    objects = pickle.load(gzip.GzipFile(
        '../validation_results/results/oblique_integration/Turi_CA1_2019/oblique_model_mean_peak_derivs_sync.p', 'rb'))
    plt.plot(inputs, objects['mean_peak_deriv'], 'o-', label=labels[2], color=colors_fig[2], zorder=0)

    objects = pickle.load(gzip.GzipFile(
        '../validation_results/results/oblique_integration/Tomko_CA1_v2_weak/oblique_model_mean_peak_derivs_sync.p',
        'rb'))
    plt.plot(inputs, objects['mean_peak_deriv'], 'o-', label=labels[3], color=colors_fig[3], zorder=2)
    plt.annotate('#5', xy=(5.15, 8.00), xytext=(5.62, 6.64), arrowprops=dict(facecolor=colors_fig[3], shrink=0.01),
                 zorder=2)

    objects = pickle.load(gzip.GzipFile(
        '../validation_results/results/oblique_integration/Migliore_CA1_pyr_08_apic[12]/oblique_model_mean_peak_derivs_sync.p',
        'rb'))
    plt.plot(inputs, objects['mean_peak_deriv'], 'o-', label=labels[4], color=colors_fig[4], zorder=4)
    plt.annotate('#5', xy=(5.15, 2.20), xytext=(5.62, 0.84), arrowprops=dict(facecolor=colors_fig[4], shrink=0.01),
                 zorder=4)

    inputs = np.arange(0, 8, 1)
    deriv = [0, 0.22, 0.74, 0.96, 1.16, 5.33, 5.5, 5.54]
    plt.plot(inputs, deriv, 'o-', label=labels_exp[-1], color=colors_fig[-1], zorder=6)
    plt.annotate('#5', xy=(5.15, 5.07), xytext=(5.62, 3.71), arrowprops=dict(facecolor=colors_fig[-1], shrink=0.01),
                 zorder=6)

    plt.ylim((0, 13))
    plt.xlabel('# of inputs')
    plt.ylabel('dV/dt (V/s)')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_5f' + '.png', format='png', bbox_inches='tight')
    plt.savefig(path_save + 'fig_5f' + '.svg', format='svg', bbox_inches='tight')


def fig_6():
    data = json.load(
        open(path_data + 'final_score.json'))

    labels = ['C10', 'C10 vTo21', 'CP15', 'CP15 vTo21', 'Tu19', 'Tu19 vTo21', 'To21', 'M18']
    colors_fig = ['tomato', 'salmon', 'goldenrod', 'gold', 'forestgreen', 'limegreen', 'darkorchid', 'navy']

    xticks_pos = np.arange(0, 6, 1)
    xticks = ['somatic_features', 'depol_block', 'PSP_attenuation', 'backpropagating_AP_strong',
              'backpropagating_AP_weak', 'oblique_integration']
    bar_width = 1.0 / (len(labels) + 1)
    tests = ['somatic_features_score', 'depol_block_score', 'PSP_attenuation_score', 'bAP_strong_score',
             'bAP_weak_score', 'oblique_integration_score']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8.27, 4))

    i = 0
    for l in labels:
        score = []
        for t in tests:
            if data[l][t] is None:
                score.append(np.nan)
            else:
                score.append(data[l][t])
        r = [x + i * bar_width for x in np.arange(len(xticks_pos))]
        plt.bar(r, score, width=bar_width, edgecolor='white', label=labels[i], color=colors_fig[i])
        i = i + 1

    plt.hlines(2, -0.27, 5.94, color='crimson')
    plt.vlines([0.89, 1.89, 2.89, 3.89, 4.89], 0, 22.5, color='gray', linestyle=':')
    plt.xlim(-0.27, 5.94)
    plt.ylim(0, 22.5)
    plt.xticks([r + bar_width * 3 for r in range(len(xticks))], xticks, rotation=45)
    plt.subplots_adjust(bottom=0.4)
    plt.ylabel('Normalized final score')
    lgd = plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_6' + '.png', format='png', bbox_inches='tight', bbox_extra_artists=(lgd,))
    plt.savefig(path_save + 'fig_6' + '.svg', format='svg', bbox_inches='tight', bbox_extra_artists=(lgd,))
    plt.close()


def fig_7():
    data = json.load(
        open(path_data + 'run_times.json'))

    labels = ['C10', 'C10 vTo21', 'CP15', 'CP15 vTo21', 'Tu19', 'Tu19 vTo21', 'To21', 'M18']
    colors_fig = ['tomato', 'salmon', 'goldenrod', 'gold', 'forestgreen', 'limegreen', 'darkorchid', 'navy']

    xticks_pos = np.arange(0, 5, 1)
    xticks = ['somatic_features', 'depol_block', 'PSP_attenuation', 'backpropagating_AP', 'oblique_integration']
    bar_width = 1.0 / (len(labels) + 1)
    tests = ['somatic_features', 'depol_block', 'PSP_attenuation', 'bAP', 'oblique_integration']

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8.27, 4))

    i = 0
    for l in labels:
        time = []
        for t in tests:
            if data[l][t] is None:
                time.append(np.nan)
            else:
                time.append(data[l][t])
        r = [x + i * bar_width for x in np.arange(len(xticks_pos))]
        ax.bar(r, time, width=bar_width, edgecolor='white', label=labels[i], color=colors_fig[i])
        i = i + 1

    ax.vlines([0.89, 1.89, 2.89, 3.89], 0, 2495, color='gray', linestyle=':')
    ax.set_xlim(-0.25, 4.95)
    ax.set_yscale('log')
    ax.set_xticks([r + bar_width * 3 for r in range(len(xticks))])
    ax.set_xticklabels(xticks)
    ax.set_ylabel('Time (s)')
    lgd = ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')

    fig.tight_layout()
    plt.savefig(path_save + 'fig_7' + '.png', format='png', bbox_inches='tight', bbox_extra_artists=(lgd,))
    plt.savefig(path_save + 'fig_7' + '.svg', format='svg', bbox_inches='tight', bbox_extra_artists=(lgd,))
    plt.close()


def main():
    fig_5a()
    fig_5b()
    fig_5c()
    fig_5d()
    fig_5e()
    fig_5f()
    fig_6()
    fig_7()
    legend()


if __name__ == '__main__':
    main()
