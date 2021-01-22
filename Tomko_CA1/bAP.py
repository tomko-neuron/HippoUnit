"""produces a simulation of the backpropagation of the action potential into the apical trunk"""

# _title_   : bAP.py
# _author_  : Matus Tomko
# _mail_    : matus.tomko __at__ fmph.uniba.sk

import efel
import matplotlib.pyplot as plt
import numpy
from neuron import h, gui
import os

savepath = './figs/'
if not os.path.exists(savepath):
    os.mkdir(savepath)

def main():

    h.nrn_load_dll('./Mods/nrnmech.dll')
    h.xopen('pyramidal_cell_extended_v2_opt_weak_bAP.hoc')
    cell = h.CA1_PC_Tomko()

    stim = h.IClamp(cell.soma[0](0.5))
    stim.delay = 500
    stim.amp = 0.8
    stim.dur = 1000

    v_vec_soma = h.Vector().record(cell.soma[0](0.5)._ref_v)
    v_vecs_apical_trunk = {}
    v_vecs_apical_trunk['50'] = h.Vector().record(cell.radTprox(0.5)._ref_v)
    v_vecs_apical_trunk['150'] = h.Vector().record(cell.radTmed(0.5)._ref_v)
    v_vecs_apical_trunk['245.45'] = h.Vector().record(cell.radTdist(0.22727272727272727)._ref_v)
    v_vecs_apical_trunk['263.63'] = h.Vector().record(cell.radTdist(0.3181818181818182)._ref_v)
    v_vecs_apical_trunk['336.36'] = h.Vector().record(cell.radTdist(0.6818181818181819)._ref_v)
    v_vecs_apical_trunk['354.54'] = h.Vector().record(cell.radTdist(0.7727272727272728)._ref_v)

    t_vec = h.Vector()
    t_vec.record(h._ref_t)

    h.dt = 0.025
    h.tstop = 1700
    h.v_init = -65
    h.celsius = 35
    h.init()
    h.run()

    traces = []
    for vec in v_vecs_apical_trunk:
        trace = {}
        trace['T'] = numpy.array(t_vec)
        trace['V'] = numpy.array(v_vecs_apical_trunk[vec])
        trace['stim_start'] = [500]
        trace['stim_end'] = [1500]
        traces.append(trace)
    efel.api.setThreshold(-52.0)
    efel_results = efel.getFeatureValues(traces, ['AP1_amp'])

    fig = plt.figure(figsize=(5, 5))
    plt.plot(t_vec, v_vec_soma, label='soma')
    for vec in v_vecs_apical_trunk:
        plt.plot(t_vec, v_vecs_apical_trunk[vec], label=vec + ' um')
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane potential (mV)')
    lgd = plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.savefig(savepath + 'traces.png', format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()

    fig = plt.figure(figsize=(5, 5))
    plt.plot(t_vec, v_vec_soma, label='soma')
    for vec in v_vecs_apical_trunk:
        plt.plot(t_vec, v_vecs_apical_trunk[vec], label=vec + ' um')
    plt.xlim((503,513))
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane potential (mV)')
    plt.title('First AP')
    lgd = plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.savefig(savepath + 'AP1_traces.png', format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()

    dist = [50, 150, 245.45, 263.63, 336.36, 354.54]
    fig = plt.figure(figsize=(5, 5))
    for i in range(len(dist)):
        plt.plot(dist[i], efel_results[i]['AP1_amp'], marker='o', linestyle='none', label=dist[i])
    plt.xlabel('Distance from the soma (um)')
    plt.ylabel('AP1_amp (mV)')
    lgd = plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    plt.savefig(savepath + 'AP1_amps.png', format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    main()