import config_files_handling.config_handler as CH
import activity_experiments_python.bee_activity as BA
import datetime 
import pandas as pd

ROOT_PATH       = '/Users/matthieu/.ssh/ssh_to_graz/wdd_beetle_testvideos/'
PARAMS_PATH     = ROOT_PATH + 'Experiments_processing/processing_parameters/'
video_file      = 'v_hive1_rpi4_230727-130000-utc.mp4'

leds_pos_file   = PARAMS_PATH + 'leds_rpi4/leds_pos.json'
fields_file     = PARAMS_PATH + 'general/fields.json'

exp_timestamp   = CH.datetime_from_filename(video_file)
leds_pos        = CH.get_leds_position(leds_pos_file, exp_timestamp)
res_fields      = CH.get_results_df_fields(fields_file)

# import matplotlib.pyplot
# BA.show_video_frame(ROOT_PATH+video_file, cropX=leds_pos['led0']['x'], cropY=leds_pos['led0']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()
# BA.show_video_frame(ROOT_PATH+video_file, cropX=leds_pos['led1']['x'], cropY=leds_pos['led1']['y'], frame_of_interest=10)
# matplotlib.pyplot.show()

led0_int = BA.compute_video_intensity(ROOT_PATH+video_file, cropX=leds_pos['led0']['x'], cropY=leds_pos['led0']['y'], frames='all')
led1_int = BA.compute_video_intensity(ROOT_PATH+video_file, cropX=leds_pos['led1']['x'], cropY=leds_pos['led1']['y'], frames='all')

res=[[]]*len(led0_int)
for int_id, intensity in enumerate(led0_int):
    int_ts = exp_timestamp + datetime.timedelta(seconds=(int_id)/30)
    params = 'cropled0={},crop_led1={}'.format(leds_pos['led0'],leds_pos['led1'])
    res[int_id] = [int_ts, None, 'LEDs intensities', 'rpi4', params, intensity, '']

res_df = pd.DataFrame(res, columns=res_fields['fields'])
res_df.to_pickle(ROOT_PATH+'/data/leds/'+exp_timestamp.strftime('%y%m%dT%H%M%S%Z')+'_leds.pickle')
# print(led0_int)

