import config_files_handling.config_handler as CH
import activity_experiments_python.bee_activity as BA
import activity_experiments_python.scenario_management as SM
import datetime
import pandas
import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True, help='required, filename of input file')
parser.add_argument('-c', '--computer', type=str, default='beetle', help='optional, name of the computer')
args = parser.parse_args()

ROOT_PATH               = '/Users/matthieu/Documents/proto3/Graz2023/May/activity/continuous/'
ROOT_PROCESSING_PATH    = '/Users/matthieu/.ssh/ssh_to_graz/'

PARAMS_PATH     = ROOT_PROCESSING_PATH + 'Experiments_processing/processing_parameters/' + args.computer + '/'
video_file      = args.file

leds_pos_file   = PARAMS_PATH + 'leds_rpi4/leds_pos.json'
fields_file     = PARAMS_PATH + 'general/fields.json'
amp_config_file = PARAMS_PATH + 'amp2config/amp_config.json'
sig_config_file = PARAMS_PATH + 'signals/signals_config.json'

exp_timestamp   = CH.datetime_from_filename(video_file)
leds_pos        = CH.get_leds_position(leds_pos_file, exp_timestamp)
res_fields      = CH.get_results_df_fields(fields_file)
amp_conf        = CH.get_amp_config(amp_config_file, exp_timestamp)
sig_conf        = CH.get_sig_config(sig_config_file, exp_timestamp)

exp_path = '/'.join(video_file.split('/')[:-1])
logfilename = [exp_path+'/'+f for f in os.listdir(exp_path) if f.endswith('.log')][0]
print(logfilename)

# Read log file
with open(logfilename) as f :
    content = f.readlines()
    f.close()

scenario = [json.loads(line.split('> ')[-1].replace("'",'"')) for line in content if "Scenario found" in line][0]
thled_0, thled_1, thtrig_0, thtrig_1 = SM.extract_scenario_data_from_raw_scenario(scenario)

leds_from_video = pandas.read_pickle(ROOT_PATH + 'processed_data/acts/leds/' + exp_timestamp.strftime("%y%m%dT%H%M%S") + "UTC_leds.pickle")
print(leds_from_video.columns)
# print(experiment_commands)
# print(amp_conf)
# print(sig_conf)

