import os
import json


def extract_signals_config(file):

    # try :
    f = open(file, "r")
    config = json.load(f)
    f.close()
    # except :
    #     print('There was a problem reading/interpreting file {}. Quitting'.format(file))
    #     return None

    return config