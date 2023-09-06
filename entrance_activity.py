import config_files_handling.config_handler as CH
import activity_experiments_python.bee_activity as BA
import activity_experiments_python.actuation_management as AM

import pandas as pd
import datetime

ROOT_PATH       = '/Users/matthieu/.ssh/ssh_to_graz/wdd_beetle_testvideos/'
COMPUTER        = 'sting'
PARAMS_PATH     = ROOT_PATH + 'Experiments_processing/processing_parameters/'+COMPUTER+'/'
video_file      = 'v_hive1_rpi5_230727-130000-utc.mp4'

tunnel_pos_file = PARAMS_PATH + 'entrance_rpi5/tunnel_pos.json'
fields_file     = PARAMS_PATH + 'general/fields.json'

exp_timestamp   = CH.datetime_from_filename(video_file)
tunnel_pos      = CH.get_tunnel_position(tunnel_pos_file, exp_timestamp)
res_fields      = CH.get_results_df_fields(fields_file)

# import matplotlib.pyplot
# BA.show_video_frame(ROOT_PATH+video_file, cropX=tunnel_pos['x'], cropY=tunnel_pos['y'], frame_of_interest=10)
# matplotlib.pyplot.show()

import cv2
import numpy

backSub = cv2.createBackgroundSubtractorKNN()
capture = cv2.VideoCapture(ROOT_PATH+video_file)
if not capture.isOpened():
    print('Unable to open: ' + video_file)
    exit(0)

FRAMES_TO_DISCARD = 10
# FRAMES_TO_PROCESS = 50
MIN_AREA = 500
LOW_THRESHOLD=50
HIGH_THRESHOLD=255
area_cnt_tot = [None]*300000
frame_cnt = 0
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    frame = frame[tunnel_pos['x'][0]:tunnel_pos['x'][1],tunnel_pos['y'][0]:tunnel_pos['y'][1]]
    fgMask = backSub.apply(frame)
    
    frame_cnt += 1
    if frame_cnt < FRAMES_TO_DISCARD:
        continue

    # if frame_cnt > FRAMES_TO_PROCESS:
    #     break

    if frame_cnt%1000 == 0:
        print(frame_cnt)

    fgMask = cv2.blur(fgMask, ksize=(5,5))
    fgMask = cv2.threshold(fgMask, LOW_THRESHOLD, HIGH_THRESHOLD, cv2.THRESH_BINARY)[1]

    analysis = cv2.connectedComponentsWithStats(fgMask, 4, cv2.CV_32S)
    (totalLabels, label_ids, values, centroid) = analysis
    output = []
    
    output_msk = numpy.zeros(frame.shape[:2], dtype=numpy.uint8)
    area_cnt = 0
    for i in range(1, totalLabels):
        area = values[i, cv2.CC_STAT_AREA]  
        # print(area)
        if (area > MIN_AREA):
            componentMask = (label_ids == i).astype("uint8") * 255
            # Creating the Final output mask
            output_msk = cv2.bitwise_or(output_msk, componentMask)
            area_cnt+= area
    

    area_cnt_tot[frame_cnt] = area_cnt 

#     cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
#     # cv2.putText(frame, str(analysis[0]-1), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
#     cv2.putText(frame, str(area_cnt), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
#     cv2.imshow('Frame', frame)
#     cv2.imshow('FG Mask', output_msk)
    
#     keyboard = cv2.waitKey(30)
#     if keyboard == 'q' or keyboard == 27:
#         break
# cv2.destroyAllWindows()


res_act = [x for x in area_cnt_tot if not(x==None)]

res=[[]]*len(res_act)
for act_id, act in enumerate(res_act):
    act_ts = exp_timestamp + datetime.timedelta(seconds=(act_id+FRAMES_TO_DISCARD)/30)
    params = 'ftd={},minarea={},low_thres={},high_thres={}'.format(FRAMES_TO_DISCARD,MIN_AREA,LOW_THRESHOLD,HIGH_THRESHOLD)
    res[act_id] = [act_ts, None, 'Entrance activity', 'rpi5', params, act, '']

res_df = pd.DataFrame(res, columns=res_fields['fields'])
res_df.to_pickle(ROOT_PATH+'/data/entrance/'+exp_timestamp.strftime('%y%m%dT%H%M%S%Z')+'_entrance.pickle')
