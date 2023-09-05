import json

import datetime
import pytz


ECHO_CODE   = False
ECHO_DEBUG  = True

def datetime_from_filename(filename):
    if not(filename.endswith('.mp4')):
        if ECHO_DEBUG:
            print("Unknown file type. Must be mp4")
        return None
    
    if ECHO_CODE:
        print("Looking for file : {}".format(filename))

    try :
        datetime_str = filename.split('_')[-1].split('.')[0]
        if ECHO_CODE:
            print("Corresponding datetime string : {}".format(datetime_str))
        datetime_object = datetime.datetime.strptime(datetime_str[:-4], "%y%m%d-%H%M%S")
        datetime_object = pytz.utc.localize(datetime_object)
    except:
        if ECHO_DEBUG:
            print("Unknown file format. Must be xxxx_datetime.mp4")
        return None
    
    return datetime_object

def get_frame_position(frame_config_fname, date_time):
    try :
        fp = open(frame_config_fname)
        frame_pos = json.load(fp)
        fp.close()
    except:
        if ECHO_DEBUG:
            print("Unable to find/read json file")
            return None
        
    for key in frame_pos.keys():
        pos = frame_pos[key]
        start_time = pytz.utc.localize(datetime.datetime.strptime(pos['from'][2:], "%y%m%dT%H%M%S"))
        stop_time = pytz.utc.localize(datetime.datetime.strptime(pos['to'][2:], "%y%m%dT%H%M%S"))
        if (date_time > start_time and date_time < stop_time):
            return pos['pos']
    if ECHO_DEBUG:
        print("Could not find a matching frame position for this time.")
    return None

def get_leds_position(leds_config_fname, date_time):
    try :
        fp = open(leds_config_fname)
        leds_pos = json.load(fp)
        fp.close()
    except:
        if ECHO_DEBUG:
            print("Unable to find/read json file")
            return None
        
    for key in leds_pos.keys():
        pos = leds_pos[key]
        start_time = pytz.utc.localize(datetime.datetime.strptime(pos['from'][2:], "%y%m%dT%H%M%S"))
        stop_time = pytz.utc.localize(datetime.datetime.strptime(pos['to'][2:], "%y%m%dT%H%M%S"))
        if (date_time > start_time and date_time < stop_time):
            return {'led0':pos['led0'], 'led1':pos['led1']}
    if ECHO_DEBUG:
        print("Could not find a matching leds position for this time.")
    return None

def get_tunnel_position(tunnel_config_fname, date_time):
    try :
        fp = open(tunnel_config_fname)
        tunnel_pos = json.load(fp)
        fp.close()
    except:
        if ECHO_DEBUG:
            print("Unable to find/read json file")
            return None
        
    for key in tunnel_pos.keys():
        pos = tunnel_pos[key]
        start_time = pytz.utc.localize(datetime.datetime.strptime(pos['from'][2:], "%y%m%dT%H%M%S"))
        stop_time = pytz.utc.localize(datetime.datetime.strptime(pos['to'][2:], "%y%m%dT%H%M%S"))
        if (date_time > start_time and date_time < stop_time):
            return pos['pos']
    if ECHO_DEBUG:
        print("Could not find a matching tunnel position for this time.")
    return None

def get_results_df_fields(fields_config_fname):
    try :
        fp = open(fields_config_fname)
        fields = json.load(fp)
        fp.close()
    except:
        if ECHO_DEBUG:
            print("Unable to find/read json file")
            return None
    
    return fields

def get_amp_config(amp_config_fname, date_time):
    try :
        fp = open(amp_config_fname)
        amp_conf = json.load(fp)
        fp.close()
    except:
        if ECHO_DEBUG:
            print("Unable to find/read json file")
            return None
        
    for key in amp_conf.keys():
        conf = amp_conf[key]
        start_time = pytz.utc.localize(datetime.datetime.strptime(conf['from'][2:], "%y%m%dT%H%M%S"))
        stop_time = pytz.utc.localize(datetime.datetime.strptime(conf['to'][2:], "%y%m%dT%H%M%S"))
        if (date_time > start_time and date_time < stop_time):
            return conf['config']
    if ECHO_DEBUG:
        print("Could not find a matching amp configuration for this time.")
    return None

def get_sig_config(sig_config_fname, date_time):
    try :
        fp = open(sig_config_fname)
        sig_conf = json.load(fp)
        fp.close()
    except:
        if ECHO_DEBUG:
            print("Unable to find/read json file")
            return None
        
    for key in sig_conf.keys():
        conf = sig_conf[key]
        start_time = pytz.utc.localize(datetime.datetime.strptime(conf['from'][2:], "%y%m%dT%H%M%S"))
        stop_time = pytz.utc.localize(datetime.datetime.strptime(conf['to'][2:], "%y%m%dT%H%M%S"))
        if (date_time > start_time and date_time < stop_time):
            return conf['config']
    if ECHO_DEBUG:
        print("Could not find a matching amp configuration for this time.")
    return None

