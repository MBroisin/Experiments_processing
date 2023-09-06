import config_files_handling.config_handler as CH
import pandas as pd

ROOT_PATH       = '/Users/matthieu/.ssh/ssh_to_graz/wdd_beetle_testvideos/'
COMPUTER        = 'sting'
PARAMS_PATH     = ROOT_PATH + 'Experiments_processing/processing_parameters/'+COMPUTER+'/'
video_file      = 'v_hive1_rpi4_230727-130000-utc.mp4'

frame_pos_file  = PARAMS_PATH + 'frame_rpi4/frame_pos.json'
leds_pos_file   = PARAMS_PATH + 'leds_rpi4/leds_pos.json'
tunnel_pos_file = PARAMS_PATH + 'entrance_rpi5/tunnel_pos.json'
fields_file     = PARAMS_PATH + 'general/fields.json'
ampconf_file    = PARAMS_PATH + 'amp2config/amp_config.json'
signals_file    = PARAMS_PATH + 'signals/signals_config.json'

exp_timestamp   = CH.datetime_from_filename(video_file)

frame_pos       = CH.get_frame_position(frame_pos_file, exp_timestamp)
leds_pos        = CH.get_leds_position(leds_pos_file, exp_timestamp)
tunnel_pos      = CH.get_tunnel_position(tunnel_pos_file, exp_timestamp)
res_fields      = CH.get_results_df_fields(fields_file)
ampconf         = CH.get_amp_config(ampconf_file, exp_timestamp)
sigconf         = CH.get_sig_config(signals_file, exp_timestamp)


print(exp_timestamp.strftime('%y%m%dT%H%M%S%Z'))