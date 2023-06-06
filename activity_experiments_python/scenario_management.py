import os
import json
import numpy
import matplotlib
import matplotlib.pyplot


def extract_scenario_data(file, fps=30, old_scenario=False):

    experiment_lineup = dict()
    if old_scenario:
        try :
            experiment_lineup = json.load(open(file))
        except:
            print('Unable to read scenario file. Quitting')
    else :
        try :
            experiment_lineup_temp = json.load(open(file))
        except:
            print('Unable to read scenario file. Quitting')
        for idline, line in enumerate(experiment_lineup_temp):
            experiment_lineup[str(idline)] = line

    # try :
    #     f = open(file, "r")
    #     lineup = json.load(f)
    #     f.close()
    # except :
    #     print('There was a problem reading/interpreting file {}. Quitting'.format(file))
    #     return None, None

    led_0 = [1]
    led_1 = [1]
    trig_0 = [11]
    trig_1 = [11]

    try :
        for key in lineup.keys():
            if not(lineup[key][0]=='trig'):
                led_0 += [led_0[-1]]*lineup[key][-1]*fps
                led_1 += [led_1[-1]]*lineup[key][-1]*fps
                trig_0 += [trig_0[-1]]*lineup[key][-1]*fps
                trig_1 += [trig_1[-1]]*lineup[key][-1]*fps
            else :
                trig_0 += [lineup[key][1]]*lineup[key][-1]*fps
                if (lineup[key][1]==11):
                    led_0 += [1]*lineup[key][-1]*fps
                else :
                    led_0 += [0]*lineup[key][-1]*fps

                trig_1 += [lineup[key][2]]*lineup[key][-1]*fps
                if (lineup[key][2]==11):
                    led_1 += [1]*lineup[key][-1]*fps
                else :
                    led_1 += [0]*lineup[key][-1]*fps

    except :
        print('Could not interpret scenario file. Quitting')
    
    return numpy.array(led_0), numpy.array(led_1), numpy.array(trig_0), numpy.array(trig_1)


def compute_time_shift(ledmeasure, ledtheory, plot=True, save_plot_fname=None, fps=30):
    # print(datapack[key])
    ledint = numpy.array(ledmeasure)
    ledint = ledint-numpy.min(ledint)
    ledint = ledint/numpy.max(ledint)
    ledtheory = numpy.array(ledtheory)
    ledtheory = ledtheory-numpy.min(ledtheory)
    ledtheory = ledtheory/numpy.max(ledtheory)

    time_shift = numpy.argmax(numpy.correlate(ledint, ledtheory,'valid'))

    if plot :
        fig = matplotlib.pyplot.figure(figsize=(12,5))
        matplotlib.pyplot.plot(numpy.array(range(ledint.shape[0]))/fps, ledint, 'g', label='Measurement')
        matplotlib.pyplot.plot(numpy.array(range(ledtheory.shape[0]))/fps, ledtheory, ':b', label='Theory')
        matplotlib.pyplot.plot((numpy.array(range(ledtheory.shape[0]))+time_shift)/fps, ledtheory, 'r', label='Theory_corrected')
        matplotlib.pyplot.legend()
        matplotlib.pyplot.title('LED visual intensity pattern and LED command pattern timing matching')
        matplotlib.pyplot.xlabel('Time [s]')
        matplotlib.pyplot.ylabel('Theoritical and observed LED intensity [-]')
        if not(save_plot_fname==None):
            matplotlib.pyplot.savefig(save_plot_fname)

    return time_shift
