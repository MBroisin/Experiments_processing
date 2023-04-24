import numpy

import matplotlib
import matplotlib.pyplot

def from_signal_to_actuator(sigconfig, SB, trig_value, ampconfig):
    actuation_pattern_element = {
        0:{},
        1:{},
        2:{},
        3:{},
        4:{},
        5:{},
        6:{},
        7:{}
    }

    SB_config = {'SB0': {'1':'sig1', '2':'sig2'}, 'SB1': {'1':'sig3', '2':'sig4'}}

    try :
        curr_sig = sigconfig[SB][str(trig_value)]
    except :
        curr_sig = {'1':{}, '2':{}}

    for key in curr_sig.keys():
        if not(curr_sig[key]=={}):
            actuators = ampconfig[SB_config[SB][key]]
            for act in actuators:
                actuation_pattern_element[act] = curr_sig[key]

    return actuation_pattern_element

def update_actuation_pattern(apattern, apel0, apel1, index):
    for actkey in apattern['signals']:
        apattern['signals'][actkey][index]={}
        apattern['onoff'][actkey][index]=0

        sig_element0 = apel0[actkey]
        sig_element1 = apel1[actkey]
        if not(sig_element0=={}):
            apattern['signals'][actkey][index] = sig_element0
            apattern['onoff'][actkey][index] = 1
        elif not(sig_element1=={}):
            apattern['signals'][actkey][index] = sig_element1
            apattern['onoff'][actkey][index] = 1

        # if index==100:
        #     print(actkey)
        #     print(sig_element1)
        #     print(apattern['signals'][5])
    return apattern


def create_actuation_pattern(trig0, trig1, ampconfig, sigconfig, plot=True):
    trig_length = trig0.shape[0]

    actuators_onoff = {
        0:[0]*trig_length,
        1:[0]*trig_length,
        2:[0]*trig_length,
        3:[0]*trig_length,
        4:[0]*trig_length,
        5:[0]*trig_length,
        6:[0]*trig_length,
        7:[0]*trig_length
    }
    actuators_signals = {
        0:[{}]*trig_length,
        1:[{}]*trig_length,
        2:[{}]*trig_length,
        3:[{}]*trig_length,
        4:[{}]*trig_length,
        5:[{}]*trig_length,
        6:[{}]*trig_length,
        7:[{}]*trig_length
    }

    actuation_pattern = {'signals':actuators_signals.copy(), 'onoff':actuators_onoff.copy()}

    for ind_t in range(trig_length):
        act_pattern_el0 = from_signal_to_actuator(sigconfig=sigconfig, SB='SB0', trig_value=trig0[ind_t], ampconfig=ampconfig)
        act_pattern_el1 = from_signal_to_actuator(sigconfig=sigconfig, SB='SB1', trig_value=trig1[ind_t], ampconfig=ampconfig)

        actuation_pattern = update_actuation_pattern(actuation_pattern, act_pattern_el0, act_pattern_el1, ind_t)
        # if ind_t == 100:
        #     print(act_pattern_el0)
        #     print(act_pattern_el1)
        #     break

    if plot :
        _, ax = matplotlib.pyplot.subplots(8, 1, figsize=(12,10))
        for idkey, key in enumerate(actuation_pattern['onoff'].keys()):
            onoff_sig = actuation_pattern['onoff'][key]
            ax[idkey].plot(range(len(onoff_sig)), onoff_sig)
            
    for key in actuation_pattern['onoff']:
        actuation_pattern['onoff'][key] = numpy.array(actuation_pattern['onoff'][key])
        actuation_pattern['signals'][key] = numpy.array(actuation_pattern['signals'][key])
    return actuation_pattern
