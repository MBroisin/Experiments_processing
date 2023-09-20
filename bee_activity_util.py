import config_files_handling.config_handler as CH
import activity_experiments_python.bee_activity as BA
import datetime 
# import pytz
import pandas as pd
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True, help='required, filename of input file')
parser.add_argument('-c', '--computer', type=str, default='beetle', help='optional, name of the computer')
parser.add_argument('-p', '--frames', type=str, default='all', help='optional, number of frames to process ("all" for all)')
args = parser.parse_args()

if args.frames == 'all':
    FRAMES_TO_PROCESS = 'all'
else :
    FRAMES_TO_PROCESS = int(args.frames)

if args.computer == 'beetle':
    ROOT_PATH   = '/home/hiveopolis/processing_broisin/overview/'
else :
    ROOT_PATH   = '/home/sting/processing_broisin/overview/'

PARAMS_PATH     = ROOT_PATH + 'Experiments_processing/processing_parameters/'+args.computer+'/'
video_file      = args.file

frame_pos_file   = PARAMS_PATH + 'frame_rpi4/frame_pos.json'
fields_file     = PARAMS_PATH + 'general/fields.json'

# exp_timestamp   = pytz.utc.localize(datetime.datetime(2023,7,22,11,00,00))
exp_timestamp   = CH.datetime_from_filename(video_file)
frame_pos       = CH.get_frame_position(frame_pos_file, exp_timestamp)
res_fields      = CH.get_results_df_fields(fields_file)

CROP_MARGIN = 20
OUTER_CROP_X = frame_pos['x']
OUTER_CROP_Y = frame_pos['y']
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
import matplotlib.pyplot
# BA.show_video_frame(ROOT_PATH+video_file, cropX=frame_pos['x'], cropY=frame_pos['y'], frame_of_interest=145)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['0']['x'], cropY=CROPS['0']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['1']['x'], cropY=CROPS['1']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['2']['x'], cropY=CROPS['2']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['3']['x'], cropY=CROPS['3']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['4']['x'], cropY=CROPS['4']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['5']['x'], cropY=CROPS['5']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['6']['x'], cropY=CROPS['6']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=CROPS['7']['x'], cropY=CROPS['7']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()

# led0_int = BA.compute_video_intensity(ROOT_PATH+video_file, cropX=leds_pos['led0']['x'], cropY=leds_pos['led0']['y'], frames='all')
# led1_int = BA.compute_video_intensity(ROOT_PATH+video_file, cropX=leds_pos['led1']['x'], cropY=leds_pos['led1']['y'], frames='all')
THRESHOLD_ACTIVITY = 10
activity = [[]]*9

# TIMING : around 11min33s for 100'000 frames - total 12min16s for 106'377 frames (zone 0)
activity[0] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['0']['x'], cropY=CROPS['0']['y'], frames=FRAMES_TO_PROCESS)
activity[1] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['1']['x'], cropY=CROPS['1']['y'], frames=FRAMES_TO_PROCESS)
activity[2] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['2']['x'], cropY=CROPS['2']['y'], frames=FRAMES_TO_PROCESS)
activity[3] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['3']['x'], cropY=CROPS['3']['y'], frames=FRAMES_TO_PROCESS)
activity[4] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['4']['x'], cropY=CROPS['4']['y'], frames=FRAMES_TO_PROCESS)
activity[5] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['5']['x'], cropY=CROPS['5']['y'], frames=FRAMES_TO_PROCESS)
activity[6] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['6']['x'], cropY=CROPS['6']['y'], frames=FRAMES_TO_PROCESS)
activity[7] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['7']['x'], cropY=CROPS['7']['y'], frames=FRAMES_TO_PROCESS)
activity[8] = BA.compute_video_activity(ROOT_PATH+video_file, threshold=THRESHOLD_ACTIVITY, cropX=CROPS['a']['x'], cropY=CROPS['a']['y'], frames=FRAMES_TO_PROCESS)

for i in range(9):
    res=[[]]*len(activity[i])
    crop_ind = str(i)
    if crop_ind=='8':
        crop_ind='a'
    for act_id, act in enumerate(activity[i]):
        act_ts = exp_timestamp + datetime.timedelta(seconds=(act_id+1)/30)
        params = 'thresold={},cropX={},cropY={},cropZone={},crop_margin={}'.format(THRESHOLD_ACTIVITY, OUTER_CROP_X, OUTER_CROP_Y, CROPS[crop_ind], CROP_MARGIN)
        res[act_id] = [act_ts, None, 'LEDs intensities', 'rpi4', params, act, '']

    res_df = pd.DataFrame(res, columns=res_fields['fields'])
    res_df.to_pickle(ROOT_PATH+'/data/acts/'+exp_timestamp.strftime('%y%m%dT%H%M%S%Z')+'_z{}_acts.pickle'.format(crop_ind))