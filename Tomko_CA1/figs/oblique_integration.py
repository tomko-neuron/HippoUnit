""" produces a simulation of the synaptic integration of 5 synchronous synapses
    in the proximal and distal location of the oblique dendrite """

# _title_   : oblique_integration.py
# _author_  : Matus Tomko
# _mail_    : matus.tomko __at__ fmph.uniba.sk

import os

from matplotlib import pyplot as plt
from neuron import h, gui, load_mechanisms

savepath = './figs/'
if not os.path.exists(savepath):
    os.mkdir(savepath)


def main():
    weight_dist = 0.0008
    weight_prox = 0.0023
    stim_start = 150
    stim_interval = 0.2
    ampa_list = []
    nmda_list = []
    nc_list = []
    ns_list = []

    # h.nrn_load_dll('./Mods/nrnmech.dll')
    load_mechanisms('./Mods/')
    h.xopen('pyramidal_cell_weak_bAP_original.hoc')
    cell = h.CA1_PC_Tomko()

    for i in range(5):
        ampa_syn_prox = h.Exp2Syn(cell.rad_t2(0.2))
        ampa_syn_prox.tau1 = 0.1
        ampa_syn_prox.tau2 = 2.0
        ampa_list.append(ampa_syn_prox)

        ampa_syn_dist = h.Exp2Syn(cell.rad_t2(0.8))
        ampa_syn_dist.tau1 = 0.1
        ampa_syn_dist.tau2 = 2.0
        ampa_list.append(ampa_syn_dist)

        nmda_syn_prox = h.NMDA_CA1_pyr_SC(cell.rad_t2(0.2))
        nmda_list.append(nmda_syn_prox)

        nmda_syn_dist = h.NMDA_CA1_pyr_SC(cell.rad_t2(0.8))
        nmda_list.append(nmda_syn_dist)

        stim_prox = h.NetStim()
        stim_prox.number = 1
        stim_prox.start = stim_start + i * stim_interval
        ns_list.append(stim_prox)

        stim_dist = h.NetStim()
        stim_dist.number = 1
        stim_dist.start = stim_start + 100 + i * stim_interval
        ns_list.append(stim_dist)

        nc_ampa_prox = h.NetCon(stim_prox, ampa_syn_prox, 0, 0, weight_prox)
        nc_list.append(nc_ampa_prox)
        nc_ampa_dist = h.NetCon(stim_dist, ampa_syn_dist, 0, 0, weight_dist)
        nc_list.append(nc_ampa_dist)

        nc_nmda_prox = h.NetCon(stim_prox, nmda_syn_prox, 0, 0, weight_prox / 2)
        nc_list.append(nc_nmda_prox)
        nc_nmda_dist = h.NetCon(stim_dist, nmda_syn_dist, 0, 0, weight_dist / 2)
        nc_list.append(nc_nmda_dist)

    v_vec_soma = h.Vector().record(cell.soma[0](0.5)._ref_v)
    v_vec_dend_prox = h.Vector().record(cell.rad_t2(0.2)._ref_v)
    v_vec_dend_dist = h.Vector().record(cell.rad_t2(0.8)._ref_v)
    t_vec = h.Vector().record(h._ref_t)

    h.dt = 0.025
    h.tstop = 500
    h.v_init = -65
    h.celsius = 35
    h.finitialize(-65)
    h.fcurrent()
    h.cvode_active(1)
    h.run()

    fig = plt.figure(figsize=(10, 5))
    ax1 = plt.subplot(121)
    plt.plot(t_vec, v_vec_soma, label='soma')
    plt.plot(t_vec, v_vec_dend_prox, label='rad_t2(0.2)')
    plt.xlim((120, 220))
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane potential (mV)')
    plt.title('proximal location')
    plt.legend()

    ax2 = plt.subplot(122, sharey=ax1)
    plt.plot(t_vec, v_vec_soma, label='soma')
    plt.plot(t_vec, v_vec_dend_dist, label='rad_t2(0.8)')
    plt.xlim((220, 320))
    plt.xlabel('Time (ms)')
    plt.title('distal location')
    plt.legend()
    # plt.show()
    plt.savefig(savepath + 'oblique_integration.png', format='png')
    plt.close()


if __name__ == '__main__':
    main()
