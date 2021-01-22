""" Script to run HippoUnit validation tests and register the results.
    Original ModelLoader class modified to run under MS Windows. """

# _title_   : __init__.py
# _author_  : Matus Tomko
# _mail_    : matus.tomko __at__ fmph.uniba.sk

from __future__ import print_function
from multiprocessing import freeze_support
from hippounit import tests
from hippounit.utils import ModelLoader
from json2html import *
from neuron import h

import collections
import json
import time
import IPython
import numpy
import numpy as np
import pkg_resources
import sciunit



class ModelLoader_CA1_Windows(ModelLoader):
    def __init__(self, name="model", mod_files_path=None):
        """ Constructor. """

        self.modelpath = mod_files_path
        self.hocpath = None
        self.libpath = mod_files_path

        self.cvode_active = False

        self.template_name = None
        self.SomaSecList_name = None
        self.max_dist_from_soma = 220
        self.v_init = -70
        self.celsius = 34

        self.name = name
        self.threshold = -20
        self.stim = None
        self.soma = None
        sciunit.Model.__init__(self, name=name)

        self.c_step_start = 0.00004
        self.c_step_stop = 0.000004
        self.c_minmax = numpy.array([0.00004, 0.04])

        self.ObliqueSecList_name = None
        self.TrunkSecList_name = None
        self.dend_loc = []  # self.dend_loc = [['dendrite[80]',0.27],['dendrite[80]',0.83],['dendrite[54]',0.16],['dendrite[54]',0.95],['dendrite[52]',0.38],['dendrite[52]',0.83],['dendrite[53]',0.17],['dendrite[53]',0.7],['dendrite[28]',0.35],['dendrite[28]',0.78]]
        self.dend_locations = collections.OrderedDict()
        self.NMDA_name = None
        self.default_NMDA_name = 'NMDA_CA1_pyr_SC'
        self.default_NMDA_path = pkg_resources.resource_filename("hippounit", "tests/default_NMDAr/")

        self.AMPA_name = None
        self.AMPA_NMDA_ratio = 2.0

        self.AMPA_tau1 = 0.1
        self.AMPA_tau2 = 2.0
        self.start = 150

        self.ns = None
        self.ampa = None
        self.nmda = None
        self.ampa_nc = None
        self.nmda_nc = None

        self.ampa_list = []
        self.nmda_list = []
        self.ns_list = []
        self.ampa_nc_list = []
        self.nmda_nc_list = []

        self.ndend = None
        self.xloc = None

        self.base_directory = '../validation_results/'  # inside current directory

        self.find_section_lists = False

    def load_mod_files(self):

        h.nrn_load_dll(self.modelpath + 'nrnmech.dll')

    def initialise(self):

        save_stdout = sys.stdout  # To supress hoc output from Jupyter notebook
        # sys.stdout=open("trash","w")
        sys.stdout = open('stdout.txt', 'w')  # rather print it to the console

        self.load_mod_files()

        if self.hocpath is None:
            raise Exception(
                "Please give the path to the hoc file (eg. model.modelpath = \"/home/models/CA1_pyr/CA1_pyr_model.hoc\")")

        h.load_file("stdrun.hoc")
        h.load_file(str(self.hocpath))

        if self.soma is None and self.SomaSecList_name is None:
            raise Exception(
                "Please give the name of the soma (eg. model.soma=\"soma[0]\"), or the name of the somatic section list (eg. model.SomaSecList_name=\"somatic\")")

        try:
            if self.template_name is not None and self.SomaSecList_name is not None:

                h('objref testcell')
                h('testcell = new ' + self.template_name)

                exec ('self.soma_ = h.testcell.' + self.SomaSecList_name)

                for s in self.soma_:
                    self.soma = h.secname()

            elif self.template_name is not None and self.SomaSecList_name is None:
                h('objref testcell')
                h('testcell = new ' + self.template_name)
                # in this case self.soma is set in the jupyter notebook
            elif self.template_name is None and self.SomaSecList_name is not None:
                exec ('self.soma_ = h.' + self.SomaSecList_name)
                for s in self.soma_:
                    self.soma = h.secname()
            # if both is None, the model is loaded, self.soma will be used
        except AttributeError:
            print ("The provided model template is not accurate. Please verify!")
        except Exception:
            print (
                "If a model template is used, please give the name of the template to be instantiated (with parameters, if any). Eg. model.template_name=CCell(\"morph_path\")")
            raise

        sys.stdout = save_stdout  # setting output back to normal

def somatic_features_test_UCL_dataset(model, base_directory):
    # Load target data
    with open('../target_features/feat_CA1_pyr_cACpyr_more_features.json') as f:
        config_pyr = json.load(f, object_pairs_hook=collections.OrderedDict)

    observation = config_pyr

    # Load stimuli file
    ttype = "CA1_pyr_cACpyr"

    stim_file = pkg_resources.resource_filename("hippounit", "tests/stimuli/somafeat_stim/stim_" + ttype + ".json")
    with open(stim_file, 'r') as f:
        config = json.load(f, object_pairs_hook=collections.OrderedDict)

    # Instantiate test class
    test = tests.SomaticFeaturesTest(observation=observation, config=config, force_run=False, show_plot=True,
                                     save_all=True, base_directory=base_directory)

    # test.specify_data_set is added to the name of the subdirectory (somaticfeat), so test runs using different data sets can be saved into different directories
    test.specify_data_set = 'UCL_data'

    # Number of parallel processes
    test.npool = 10

    try:
        # Run the test
        score = test.judge(model)
        # Summarize and print the score achieved by the model on the test using SciUnit's summarize function
        score.summarize()
    except Exception as e:
        print('Model: ' + model.name + ' could not be run')
        print(e)
        pass

def somatic_features_test_JMakara_dataset(model, base_directory):
    # Load target data
    with open('../target_features/feat_rat_CA1_JMakara_more_features.json') as f:
        config_pyr = json.load(f, object_pairs_hook=collections.OrderedDict)

    observation = config_pyr

    # Load stimuli file
    stim_file = pkg_resources.resource_filename("hippounit", "tests/stimuli/somafeat_stim/stim_rat_CA1_PC_JMakara.json")
    with open(stim_file, 'r') as f:
        config = json.load(f, object_pairs_hook=collections.OrderedDict)

    # Instantiate test class
    test = tests.SomaticFeaturesTest(observation=observation, config=config, force_run=False, show_plot=True,
                                     save_all=True, base_directory=base_directory)

    # test.specify_data_set is added to the name of the subdirectory (somaticfeat), so test runs using different data sets can be saved into different directories
    test.specify_data_set = 'JMakara_data'

    # Number of parallel processes
    test.npool = 10

    try:
        # Run the test
        score = test.judge(model)
        # Summarize and print the score achieved by the model on the test using SciUnit's summarize function
        score.summarize()
    except Exception as e:
        print('Model: ' + model.name + ' could not be run')
        print(e)
        pass

def PSP_attenuatuion_test(model, base_directory):
    # Load target data
    with open("../target_features/feat_PSP_attenuation_target_data.json", 'r') as f:
        observation = json.load(f, object_pairs_hook=collections.OrderedDict)

    IPython.display.HTML(json2html.convert(json=observation))

    # Load stimuli file
    stim_file = pkg_resources.resource_filename("hippounit",
                                                "tests/stimuli/PSP_attenuation_stim/stim_PSP_attenuation_test.json")

    with open(stim_file, 'r') as f:
        config = json.load(f, object_pairs_hook=collections.OrderedDict)

    # Instantiate test class
    test = tests.PSPAttenuationTest(config=config, observation=observation, num_of_dend_locations=15, force_run=False,
                                    show_plot=True, save_all=True, base_directory=base_directory)

    # Number of parallel processes
    test.npool = 10

    try:
        # Run the test
        score = test.judge(model)
        # Summarize and print the score achieved by the model on the test using SciUnit's summarize function
        score.summarize()
    except Exception as e:
        print('Model: ' + model.name + ' could not be run')
        print(e)
        pass

def backprop_AP_test(model, base_directory):
    # Load target data
    with open('../target_features/feat_backpropagating_AP_target_data.json') as f:
        observation = json.load(f, object_pairs_hook=collections.OrderedDict)

    # observation = config['features']
    IPython.display.HTML(json2html.convert(json=observation))

    # Load stimuli file
    stim_file = pkg_resources.resource_filename("hippounit", "tests/stimuli/bAP_stim/stim_bAP_test.json")

    with open(stim_file, 'r') as f:
        config = json.load(f, object_pairs_hook=collections.OrderedDict)

    # Instantiate the test class
    test = tests.BackpropagatingAPTest(config=config, observation=observation, force_run=False,
                                       force_run_FindCurrentStim=False, show_plot=True, save_all=True,
                                       base_directory=base_directory)
    # Number of parallel processes
    test.npool = 10

    try:
        # Run the test
        score = test.judge(model)
        # Summarize and print the score achieved by the model on the test using SciUnit's summarize function
        score.summarize()
    except Exception as e:
        print('Model: ' + model.name + ' could not be run')
        print(e)
        pass

def depolarization_block_test(model, base_directory):
    # Load target data
    with open('../target_features/depol_block_target_data.json') as f:
        observation = json.load(f, object_pairs_hook=collections.OrderedDict)

    # observation = config['features']
    IPython.display.HTML(json2html.convert(json=observation))

    # Instantiate the test class

    test = tests.DepolarizationBlockTest(observation=observation, force_run=False, show_plot=True, save_all=True,
                                         base_directory=base_directory)

    # Number of parallel processes
    test.npool = 10

    try:
        # Run the test
        score = test.judge(model)
        # Summarize and print the score achieved by the model on the test using SciUnit's summarize function
        score.summarize()
    except Exception as e:
        print('Model: ' + model.name + ' could not be run')
        print(e)
        pass

def oblique_integration_test(model, base_directory):
    # Load target data
    with open('../target_features/oblique_target_data.json') as f:
        observation = json.load(f, object_pairs_hook=collections.OrderedDict)

    IPython.display.HTML(json2html.convert(json=observation))

    # setting synapse parameters

    # If model.AMPA_name and/or model.NMDA_name is set here, the model's own receptor models (mod files) are used.
    # If these are not set, HippoUnit's default synapse model is used. (AMPA: NEURON's Exp2Syn, NMDA: https://github.com/KaliLab/hippounit/blob/master/hippounit/tests/default_NMDAr/NMDA_CA1_pyr_SC.mod)

    # Similarly to HippoUnit's default synapse, this model used the NEURON's Exp2Syn function as synaptic input,
    # so here the same time constants are used as originally in the model.
    # As the model doesn't have an NMDA receptor model, the default one of HippoUnit is used as the NMDA component of the synapse

    model.AMPA_tau1 = 0.4
    model.AMPA_tau2 = 1

    # Instantiate the test class
    test = tests.ObliqueIntegrationTest(observation=observation, save_all=True, force_run_synapse=False,
                                        force_run_bin_search=False, show_plot=True, base_directory=base_directory)

    # Number of parallel processes
    test.npool = 10

    try:
        # Run the test
        score = test.judge(model)
        # Summarize and print the score achieved by the model on the test using SciUnit's summarize function
        score.summarize()
    except Exception as e:
        print('Model: ' + model.name + ' could not be run')
        print(e)
        pass

def bAP_traces():
    from neuron import h
    h.nrn_load_dll('./Mods/nrnmech.dll')
    h.xopen('CA1PC.hoc')
    cell = h.CA1PyramidalCell()

    stim = h.IClamp(cell.soma(0.5))
    stim.delay = 500
    stim.amp = 1.0
    stim.dur = 400

    h.distance(0, cell.soma(1))
    print(str('radTprox(0.5): dist = ' + str(h.distance(0.5, sec=cell.radTprox))))
    print(str('radTmed(0.5):  dist = ' + str(h.distance(0.5, sec=cell.radTmed))))
    print(str('radTdist(0.3): dist = ' + str(h.distance(0.3, sec=cell.radTdist))))
    print(str('radTdist(0.7): dist = ' + str(h.distance(0.7, sec=cell.radTdist))))

    v_vec_soma = h.Vector().record(cell.soma(0.5)._ref_v)
    v_vec_radTprox = h.Vector().record(cell.radTprox(0.5)._ref_v)
    v_vec_radTmed = h.Vector().record(cell.radTmed(0.5)._ref_v)
    v_vec_radTdist_1 = h.Vector().record(cell.radTdist(0.3)._ref_v)
    v_vec_radTdist_2 = h.Vector().record(cell.radTdist(0.7)._ref_v)

    t_vec = h.Vector()
    t_vec.record(h._ref_t)

    h.dt = 0.2
    h.tstop = 1100
    h.v_init = -65
    h.celsius = 35
    h.run()

    import numpy, pickle, gzip

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

    pickle.dump(traces, gzip.GzipFile('E:/NeuronCA1/CA1_NetPyNE/Code/HippoUnit/validation_results/temp_data/backpropagating_AP/'
        'Cutsuridis_Poirazi_CA1_2015_time/cclamp_1.0.p', "wb"))


def main():
    times = []
    for i in range(1):
        # path to mod files
        mod_files_path = './Mods/'

        #all the outputs will be saved here. It will be an argument to the test.
        base_directory = '../validation_results/'

        #Load cell model
        model = ModelLoader_CA1_Windows(mod_files_path = mod_files_path)

        # outputs will be saved in subfolders named like this:
        model.name = 'Cutsuridis_Poirazi_CA1_2015_time'

        # path to hoc file
        # the model must not display any GUI!!
        model.hocpath = 'CA1PC.hoc'

        # If the hoc file doesn't contain a template, this must be None (the default value is None)
        model.template_name = 'CA1PyramidalCell()'

        # model.SomaSecList_name should be None, if there is no Section List in the model for the soma, or if the name of the soma section is given by setting model.soma (the default value is None)
        model.SomaSecList_name = 'soma'
        # if the soma is not in a section list or to use a specific somatic section, add its name here:
        model.soma = None

        # For the PSP Attenuation Test, and Back-propagating AP Test a section list containing the trunk sections is needed
        model.TrunkSecList_name = 'trunk_sec_list'
        # For the Oblique Integration Test a section list containing the oblique dendritic sections is needed
        model.ObliqueSecList_name = 'oblique_dendrites'

        # It is important to set the v_init and the celsius parameters of the simulations here,
        # as if they are only set in the model's files, they will be overwritten with the default values of the ModelLoader class.
        # default values: v_init = -70, celsius = 34
        model.v_init = -65
        model.celsius = 35

        start_time = time.time()

        somatic_features_test_UCL_dataset(model=model, base_directory=base_directory)
        somatic_features_test_JMakara_dataset(model=model, base_directory=base_directory)
        PSP_attenuatuion_test(model=model, base_directory=base_directory)
        backprop_AP_test(model=model, base_directory=base_directory)
        depolarization_block_test(model=model, base_directory=base_directory)
        oblique_integration_test(model=model, base_directory=base_directory)

        stop_time = time.time()
        print('Execution time: ' + str(stop_time - start_time) + ' seconds')
        times.append(stop_time - start_time)

    print('Execution times: ' + str(times))
    print('Average execution time: ' + str(np.average(times)) + ' seconds')

if __name__ == '__main__':
    freeze_support()
    main()
    # bAP_traces()