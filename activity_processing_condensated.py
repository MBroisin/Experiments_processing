import numpy
import cv2

import matplotlib
import matplotlib.pyplot
import matplotlib.patches

import scipy
import scipy.ndimage
import scipy.interpolate
import scipy.signal

import os
import time
import io

import sys
import pickle
import tqdm
import math

import activity_experiments_python.bee_activity as BA
import activity_experiments_python.scenario_management as SFM
import activity_experiments_python.ampconfig_management as ACM
import activity_experiments_python.signalsconfig_management as SCM
import activity_experiments_python.actuation_management as AM


# General constants
DATA_RECALCULATION_RPI = True
DATA_RECALCULATION_LEDS = False
FRAMES_TO_PROCESS = 'all'
N_FPS = 30

DATA_FOLDER = '/Users/matthieu/Documents/proto3/Graz2023/April/Activity_experiments/'
DATE_FOLDER = '20230423/'

FOLDER_AMP2 = 'Amp2config/'
FILENAME_AMP2 = 'config.json'
FOLDER_DATA = 'data/'
FOLDER_SIGNALS = 'signals/'
FILENAME_SIGNALS = 'signals_config.json'
FOLDER_SCENARIO = 'scenario/'

ACTIVITY_THRESHOLD = 5

# EXPERIMENTS = ['3/', '4/', '5/', '6/', '7/']
EXPERIMENTS = ['5/']#, '4/', '5/', '6/', '7/']

for exp_of_interest in range(len(EXPERIMENTS)):
    exp_folder = DATA_FOLDER+DATE_FOLDER+EXPERIMENTS[exp_of_interest]

    # Folder structure creation
    fpath = exp_folder+'/processed_data/'
    try:
        os.mkdir(fpath)
    except OSError:
        print ("Creation of the directory %s failed" % fpath)
    else:
        print ("Successfully created the directory %s " % fpath)
            
        
    dpath = fpath + 'activity/'
    try:
        os.mkdir(dpath)
    except OSError:
        print ("Creation of the directory %s failed" % dpath)
    else:
        print ("Successfully created the directory %s " % dpath)


    vpath = dpath + 'visualization/'
    try:
        os.mkdir(vpath)
    except OSError:
        print ("Creation of the directory %s failed" % vpath)
    else:
        print ("Successfully created the directory %s " % vpath)


    gpath = dpath + 'graphs/'
    try:
        os.mkdir(gpath)
    except OSError:
        print ("Creation of the directory %s failed" % gpath)
    else:
        print ("Successfully created the directory %s " % gpath)
    

    available_replicates = [x for x in os.listdir(exp_folder+FOLDER_DATA) if os.path.isdir(exp_folder+FOLDER_DATA+x)]

    for rep_of_interest in range(len(available_replicates)):
        times_folder = exp_folder+FOLDER_DATA+available_replicates[rep_of_interest]+'/'

        available_times = [x for x in os.listdir(times_folder) if os.path.isdir(times_folder+x)]
        time_of_interest = 0
        video_folder = times_folder+available_times[time_of_interest]+'/'

        available_videos = [x for x in os.listdir(video_folder) if x.endswith('.mp4')]
        videos = {}
        for i in range(1,6):
            rpi_name = 'rpi{}'.format(i)
            videos[rpi_name] = [video_folder+x for x in available_videos if 'hive1_rpi{}'.format(i) in x]
            if not(videos[rpi_name] == []):
                videos[rpi_name] = videos[rpi_name][0]

        print(videos)
        rpi_of_interest = 'rpi4'

        if videos[rpi_of_interest]==[]:
            continue


        OUTER_CROP_X = [467,869]
        OUTER_CROP_Y = [589,1307]
        CROP_MARGIN = 10

        mapping_index = {7:0, 6:1, 5:2, 4:3, 0:4, 1:5, 2:6, 3:7}
        CROPS = {
            '0' : {'x' : [], 'y' : []},
            '1' : {'x' : [], 'y' : []},
            '2' : {'x' : [], 'y' : []},
            '3' : {'x' : [], 'y' : []},
            '4' : {'x' : [], 'y' : []},
            '5' : {'x' : [], 'y' : []},
            '6' : {'x' : [], 'y' : []},
            '7' : {'x' : [], 'y' : []},
            'a' : {'x' : [], 'y' : []}
        }

        for key in CROPS:
            try : 
                key_int = int(key)
            except :
                key_int = -1
            if not(key_int == -1):
                posx = math.floor(mapping_index[key_int]/4)
                posy = mapping_index[key_int]%4
                # print('key {} : ({},{})'.format(key, posx, posy))
                CROPS[key]['x'] = [int((OUTER_CROP_X[1]-OUTER_CROP_X[0])/2*posx+CROP_MARGIN/2)+OUTER_CROP_X[0], int((OUTER_CROP_X[1]-OUTER_CROP_X[0])/2*(posx+1)-CROP_MARGIN/2)+OUTER_CROP_X[0]]
                CROPS[key]['y'] = [int((OUTER_CROP_Y[1]-OUTER_CROP_Y[0])/4*posy+CROP_MARGIN/2)+OUTER_CROP_Y[0], int((OUTER_CROP_Y[1]-OUTER_CROP_Y[0])/4*(posy+1)-CROP_MARGIN/2)+OUTER_CROP_Y[0]]
            else :
                posx = math.floor(mapping_index[6]/4)
                posy = mapping_index[6]%4
                CROPS[key]['x'] = [int(CROP_MARGIN/2)+OUTER_CROP_X[0], -int(CROP_MARGIN/2)+OUTER_CROP_X[1]]
                CROPS[key]['y'] = [int(CROP_MARGIN/2)+OUTER_CROP_Y[0], -int(CROP_MARGIN/2)+OUTER_CROP_Y[1]]


        if DATA_RECALCULATION_RPI:
            datapack = {}
            
            for key in CROPS.keys():
                activities = BA.compute_video_activity(videos[rpi_of_interest], threshold=ACTIVITY_THRESHOLD, frames=FRAMES_TO_PROCESS, cropX=CROPS[key]['x'], cropY=CROPS[key]['y'], video_save=True, video_filename='actvisu_'+available_replicates[rep_of_interest]+'_'+rpi_of_interest+'_actzone_'+key+'.mp4', video_foldername=vpath)
                datapack[key] = {}
                datapack[key]['act'] = activities
                datapack[key]['fname'] = videos[rpi_of_interest]
                datapack[key]['crop'] = CROPS[key]
                datapack[key]['pos'] = key
                datapack[key]['threshold'] = ACTIVITY_THRESHOLD
            
            with open(dpath + available_replicates[rep_of_interest]+'_'+rpi_of_interest+'_activities.json', 'wb') as fp:
                pickle.dump(datapack, fp)
        else :
            with open(dpath + available_replicates[rep_of_interest]+'_'+rpi_of_interest+'_activities.json', 'rb') as fp:
                datapack = pickle.load(fp)

        LED_CROPS = {
            '0' : {'x' : [554,570], 'y' : [381,397]},
            '1' : {'x' : [728,742], 'y' : [381,397]}
        }

        if DATA_RECALCULATION_LEDS:
            leds_datapack = {}
            
            for key in LED_CROPS.keys():
                activities = BA.compute_video_intensity(videos['rpi4'], frames='all', cropX=LED_CROPS[key]['x'], cropY=LED_CROPS[key]['y'])
                leds_datapack[key] = {}
                leds_datapack[key]['act'] = activities
                leds_datapack[key]['fname'] = videos['rpi4']
                leds_datapack[key]['crop'] = LED_CROPS[key]
                leds_datapack[key]['pos'] = key
            
            with open(dpath + available_replicates[rep_of_interest]+'_leds_intensities.json', 'wb') as fp:
                pickle.dump(leds_datapack, fp)
        else :
            with open(dpath + available_replicates[rep_of_interest]+'_leds_intensities.json', 'rb') as fp:
                leds_datapack = pickle.load(fp)


        scenario_folder = exp_folder+FOLDER_SCENARIO
        scenario_file = [x for x in os.listdir(scenario_folder) if x.endswith('.txt')][0]

        print('Processing scenario file : '+scenario_file)

        theory_l0, theory_l1, theory_trig0, theory_trig1 = SFM.extract_scenario_data(scenario_folder+scenario_file)
        theory_leds = {'0':theory_l0, '1':theory_l1}
        theory_leds['times'] = numpy.array(range(theory_leds['0'].shape[0]))

        theory_trigs = {'0':theory_trig0, '1':theory_trig1}
        theory_trigs['times'] = numpy.array(range(theory_trigs['0'].shape[0]))


        actuation_zones = scipy.ndimage.measurements.label(numpy.maximum(numpy.logical_not(theory_l0).astype(numpy.uint8), numpy.logical_not(theory_l1).astype(numpy.uint8)))

        print('--> {} actuation zones found.'.format(actuation_zones[1]))

        amp_config = ACM.extract_amp_config(exp_folder+FOLDER_AMP2+FILENAME_AMP2)
        signals_config = SCM.extract_signals_config(exp_folder+FOLDER_SIGNALS+FILENAME_SIGNALS)

        actuation_pattern = AM.create_actuation_pattern(theory_trig0, theory_trig1, amp_config, signals_config, save_plot_fname=gpath+available_replicates[rep_of_interest]+'_actuation_pattern.png')
        actuation_pattern['times'] = theory_trigs['times']

        shifts = []

        for idkey, key in enumerate(leds_datapack.keys()):
            shifts.append(SFM.compute_time_shift(leds_datapack[key]['act'], theory_leds[key], save_plot_fname=gpath+available_replicates[rep_of_interest]+'_led'+key+'_pattern_matching.png'))

        led_time_shift = numpy.mean(numpy.array(shifts))
        print(led_time_shift)

        theory_leds['corrected_times'] = theory_leds['times']+led_time_shift
        theory_trigs['corrected_times'] = theory_trigs['times']+led_time_shift
        actuation_pattern['corrected_times'] = actuation_pattern['times']+led_time_shift

        max_range = 0.09
        fig, ax = matplotlib.pyplot.subplots(9, 1, figsize=(12,12), sharex=True)
        for idkey, key in enumerate(datapack.keys()):
            activity = datapack[key]['act']
            ax[idkey].plot(numpy.array(range(len(activity)))/N_FPS, activity, label='Act '+key+' raw activity')
            
            ax[idkey].plot(numpy.array(range(len(activity)))/N_FPS, scipy.ndimage.gaussian_filter(numpy.array(activity), 3), label='Act '+key+' GF activity')
            # ax[idkey].plot(theory_leds['corrected_times'], theory_leds['0']*max(activity), 'm')
            # ax[idkey].plot(theory_leds['corrected_times'], theory_leds['1']*max(activity), 'g')
            try:
                ax[idkey].plot(numpy.array(actuation_pattern['corrected_times'])/N_FPS, actuation_pattern['onoff'][int(key)]*0.8*max_range, 'g', label='Actuation pattern')
            except:
                pass
            # ax[idkey].set_title(datapack[key]['pos'])
            ax[idkey].set_ylim([0, max_range])
            ax[idkey].set_xlim([-5, len(activity)/N_FPS+25])
            ax[idkey].legend(loc='upper right')

        ax[0].set_title('Activity computations in each actuator region and for the entire comb')
        matplotlib.pyplot.xlabel('Time [s]')
        ax[4].set_ylabel('Activity in percentage of pixel change per region [-]')
        matplotlib.pyplot.savefig(gpath+available_replicates[rep_of_interest]+'_activity_'+rpi_of_interest+'.png')