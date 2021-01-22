""" Produces modified bAP Test of HippoUnit """

# _title_   : bAP_test_CP15.py
# _author_  : Matus Tomko
# _mail_    : matus.tomko __at__ fmph.uniba.sk

import collections
import efel
import gzip
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pickle
from neuron import h

matplotlib.use('Agg')


def main():
    traces = run_cclamp()
    extract_features_calculate_errors(traces)


def run_cclamp():
    h.nrn_load_dll('./Mods/nrnmech.dll')
    h.xopen('CA1PC.hoc')
    cell = h.CA1PyramidalCell()

    stim = h.IClamp(cell.soma(0.5))
    stim.delay = 500
    stim.amp = 1.0
    stim.dur = 1000

    v_vec_soma = h.Vector().record(cell.soma(0.5)._ref_v)
    v_vec_radTprox = h.Vector().record(cell.radTprox(0.5)._ref_v)
    v_vec_radTmed = h.Vector().record(cell.radTmed(0.5)._ref_v)
    v_vec_radTdist_1 = h.Vector().record(cell.radTdist(0.3)._ref_v)
    v_vec_radTdist_2 = h.Vector().record(cell.radTdist(0.7)._ref_v)

    t_vec = h.Vector()
    t_vec.record(h._ref_t)

    h.dt = 0.2
    h.tstop = 1700
    h.v_init = -65
    h.celsius = 35
    h.run()

    plt.plot(t_vec, v_vec_soma, label='soma')
    plt.plot(t_vec, v_vec_radTprox, label="('CA1PyramidalCell[0].radTprox', 0.5) at 50 um")
    plt.plot(t_vec, v_vec_radTmed, label="('CA1PyramidalCell[0].radTmed', 0.5) at 150 um")
    plt.plot(t_vec, v_vec_radTdist_1, label="('CA1PyramidalCell[0].radTdist', 0.3) at 260 um")
    plt.plot(t_vec, v_vec_radTdist_2, label="('CA1PyramidalCell[0].radTdist', 0.5) at 340 um")
    plt.xlabel("time (ms)")
    plt.ylabel("membrane potential (mV)")
    lgd = plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.savefig('../validation_results/figs/backpropagating_AP/Cutsuridis_Poirazi_CA1_2015/' + 'traces.pdf',
                format='pdf', dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()

    traces = {}
    traces['T'] = numpy.array(t_vec)
    traces['v_stim'] = numpy.array(v_vec_soma)

    od = collections.OrderedDict()
    od1 = collections.OrderedDict()
    od[('CA1PyramidalCell[0].radTprox', 0.5)] = numpy.array(v_vec_radTprox)
    od1[50] = od
    od = collections.OrderedDict()
    od[('CA1PyramidalCell[0].radTmed', 0.5)] = numpy.array(v_vec_radTmed)
    od1[150] = od
    od = collections.OrderedDict()
    od[('CA1PyramidalCell[0].radTdist', 0.3)] = numpy.array(v_vec_radTdist_1)
    od1[260] = od
    od = collections.OrderedDict()
    od[('CA1PyramidalCell[0].radTdist', 0.7)] = numpy.array(v_vec_radTdist_2)
    od1[340] = od
    traces['v_rec'] = od1

    pickle.dump(traces,
                gzip.GzipFile('../validation_results/temp_data/backpropagating_AP/'
                              'Cutsuridis_Poirazi_CA1_2015/cclamp_1.0.p', "wb"))

    traces_for_efel = []

    trace_radTprox = {}
    trace_radTprox['T'] = numpy.array(t_vec)
    trace_radTprox['V'] = numpy.array(v_vec_radTprox)
    trace_radTprox['stim_start'] = [500]
    trace_radTprox['stim_end'] = [1500]
    traces_for_efel.append(trace_radTprox)

    trace_radTmed = {}
    trace_radTmed['T'] = numpy.array(t_vec)
    trace_radTmed['V'] = numpy.array(v_vec_radTmed)
    trace_radTmed['stim_start'] = [500]
    trace_radTmed['stim_end'] = [1500]
    traces_for_efel.append(trace_radTmed)

    trace_radTdist1 = {}
    trace_radTdist1['T'] = numpy.array(t_vec)
    trace_radTdist1['V'] = numpy.array(v_vec_radTdist_1)
    trace_radTdist1['stim_start'] = [500]
    trace_radTdist1['stim_end'] = [1500]
    traces_for_efel.append(trace_radTdist1)

    trace_radTdist2 = {}
    trace_radTdist2['T'] = numpy.array(t_vec)
    trace_radTdist2['V'] = numpy.array(v_vec_radTdist_2)
    trace_radTdist2['stim_start'] = [500]
    trace_radTdist2['stim_end'] = [1500]
    traces_for_efel.append(trace_radTdist2)

    return traces_for_efel


def extract_features_calculate_errors(traces):
    traces_results = efel.getFeatureValues(traces, ['AP1_amp', 'APlast_amp'])

    target_features = json.load(open("../target_features/feat_backpropagating_AP_target_data.json"))
    model_features = collections.OrderedDict()
    errors = collections.OrderedDict()
    ap1_strong_errors = []
    ap1_weak_errors = []
    aplast_errors = []

    trace_results = traces_results[0]
    d_features = {}
    p_value = trace_results['AP1_amp'][0]
    o_mean = target_features["mean_AP1_amp_at_50um"].split(" ")
    o_mean = float(o_mean[0])
    o_std = target_features["std_AP1_amp_at_50um"].split(" ")
    o_std = float(o_std[0])
    error = abs(p_value - o_mean) / o_std
    d_features['AP1_amp'] = p_value
    errors["AP1_amp_at_50"] = error
    ap1_weak_errors.append(error)
    ap1_strong_errors.append(error)

    p_value = trace_results['APlast_amp'][0]
    o_mean = target_features["mean_APlast_amp_at_50um"].split(" ")
    o_mean = float(o_mean[0])
    o_std = target_features["std_APlast_amp_at_50um"].split(" ")
    o_std = float(o_std[0])
    error = abs(p_value - o_mean) / o_std
    d_features['APlast_amp'] = p_value
    errors["APlast_amp_at_50"] = error
    aplast_errors.append(error)
    d_features['actual_distance'] = 50.0
    model_features["('CA1PyramidalCell[0].radTprox', 0.5)"] = d_features

    trace_results = traces_results[1]
    d_features = {}
    p_value = trace_results['AP1_amp'][0]
    o_mean = target_features["mean_AP1_amp_at_150um"].split(" ")
    o_mean = float(o_mean[0])
    o_std = target_features["std_AP1_amp_at_150um"].split(" ")
    o_std = float(o_std[0])
    error = abs(p_value - o_mean) / o_std
    d_features['AP1_amp'] = p_value
    errors["AP1_amp_at_150"] = error
    ap1_weak_errors.append(error)
    ap1_strong_errors.append(error)

    p_value = trace_results['APlast_amp'][0]
    o_mean = target_features["mean_APlast_amp_at_150um"].split(" ")
    o_mean = float(o_mean[0])
    o_std = target_features["std_APlast_amp_at_150um"].split(" ")
    o_std = float(o_std[0])
    error = abs(p_value - o_mean) / o_std
    d_features['APlast_amp'] = p_value
    errors["APlast_amp_at_150"] = error
    aplast_errors.append(error)
    d_features['actual_distance'] = 150.0
    model_features["('CA1PyramidalCell[0].radTmed', 0.5)"] = d_features

    trace_results = traces_results[2]
    d_features = {}
    p_value = trace_results['AP1_amp'][0]
    o_mean = target_features["mean_AP1_amp_at_250um"].split(" ")
    o_mean = float(o_mean[0])
    o_std = target_features["std_AP1_amp_at_250um"].split(" ")
    o_std = float(o_std[0])
    error = abs(p_value - o_mean) / o_std
    d_features['AP1_amp'] = p_value
    errors["AP1_amp_at_250"] = error
    ap1_weak_errors.append(error)
    ap1_strong_errors.append(error)

    p_value = trace_results['APlast_amp'][0]
    o_mean = target_features["mean_APlast_amp_at_250um"].split(" ")
    o_mean = float(o_mean[0])
    o_std = target_features["std_APlast_amp_at_250um"].split(" ")
    o_std = float(o_std[0])
    error = abs(p_value - o_mean) / o_std
    d_features['APlast_amp'] = p_value
    errors["APlast_amp_at_250"] = error
    aplast_errors.append(error)
    d_features['actual_distance'] = 260.0
    model_features["('CA1PyramidalCell[0].radTdist', 0.3)"] = d_features

    trace_results = traces_results[3]
    d_features = {}
    p_value = trace_results['AP1_amp'][0]
    o_mean_weak = target_features["mean_AP1_amp_weak_propagating_at_350um"].split(" ")
    o_mean_weak = float(o_mean_weak[0])
    o_std_weak = target_features["std_AP1_amp_weak_propagating_at_350um"].split(" ")
    o_std_weak = float(o_std_weak[0])
    error_weak = abs(p_value - o_mean_weak) / o_std_weak
    o_mean_strong = target_features["mean_AP1_amp_strong_propagating_at_350um"].split(" ")
    o_mean_strong = float(o_mean_strong[0])
    o_std_strong = target_features["std_AP1_amp_strong_propagating_at_350um"].split(" ")
    o_std_strong = float(o_std_strong[0])
    error_strong = abs(p_value - o_mean_strong) / o_std_strong
    d_features['AP1_amp'] = p_value
    errors["AP1_amp_weak_propagating_at_350"] = error_weak
    errors["AP1_amp_strong_propagating_at_350"] = error_strong
    ap1_weak_errors.append(error_weak)
    ap1_strong_errors.append(error_strong)

    p_value = trace_results['APlast_amp'][0]
    o_mean = target_features["mean_APlast_amp_at_350um"].split(" ")
    o_mean = float(o_mean[0])
    o_std = target_features["std_APlast_amp_at_350um"].split(" ")
    o_std = float(o_std[0])
    error = abs(p_value - o_mean) / o_std
    d_features['APlast_amp'] = p_value
    errors["APlast_amp_at_350"] = error
    aplast_errors.append(error)
    d_features['actual_distance'] = 340.0
    model_features["('CA1PyramidalCell[0].radTdist', 0.7)"] = d_features

    avg_weak_score = numpy.nanmean(ap1_weak_errors + aplast_errors)
    avg_strong_score = numpy.nanmean(ap1_strong_errors + aplast_errors)
    model_score = {}
    model_score["Z_score_avg_strong_propagating"] = avg_strong_score
    model_score["Z_score_avg_weak_propagating"] = avg_weak_score

    json.dump(model_features, open(
        "../validation_results/results/backpropagating_AP/Cutsuridis_Poirazi_CA1_2015/bAP_model_features.json", "w"),
              indent=4)
    json.dump(errors,
              open("../validation_results/results/backpropagating_AP/Cutsuridis_Poirazi_CA1_2015/bAP_errors.json", "w"),
              indent=4)
    json.dump(model_score,
              open("../validation_results/results/backpropagating_AP/Cutsuridis_Poirazi_CA1_2015/bAP_scores.json", "w"),
              indent=4)


if __name__ == '__main__':
    main()
