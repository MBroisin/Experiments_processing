import config_files_handling.config_handler as CH
import activity_experiments_python.bee_activity as BA
import activity_experiments_python.actuation_management as AM

ROOT_PATH       = '/Users/matthieu/.ssh/ssh_to_graz/wdd_beetle_testvideos/'
PARAMS_PATH     = ROOT_PATH + 'Experiments_processing/processing_parameters/'
video_file      = 'v_hive1_rpi5_230727-130000-utc.mp4'

tunnel_pos_file = PARAMS_PATH + 'entrance_rpi5/tunnel_pos.json'
fields_file     = PARAMS_PATH + 'general/fields.json'

exp_timestamp   = CH.datetime_from_filename(video_file)
tunnel_pos      = CH.get_tunnel_position(tunnel_pos_file, exp_timestamp)

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
area_cnt_tot = [[]]*300000
frame_cnt = 0
old_msk = []
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    frame = frame[tunnel_pos['x'][0]:tunnel_pos['x'][1],tunnel_pos['y'][0]:tunnel_pos['y'][1]]
    fgMask = backSub.apply(frame)
    
    frame_cnt += 1
    if frame_cnt < FRAMES_TO_DISCARD:
        continue

    if frame_cnt%1000 == 0:
        print(frame_cnt)

    fgMask = cv2.blur(fgMask, ksize=(5,5))
    fgMask = cv2.threshold(fgMask, 50, 255, cv2.THRESH_BINARY)[1]

    analysis = cv2.connectedComponentsWithStats(fgMask, 4, cv2.CV_32S)
    (totalLabels, label_ids, values, centroid) = analysis
    output = []
    
    output_msk = numpy.zeros(frame.shape[:2], dtype=numpy.uint8)
    area_cnt = 0
    for i in range(1, totalLabels):
        area = values[i, cv2.CC_STAT_AREA]  
        # print(area)
        if (area > 500):
            componentMask = (label_ids == i).astype("uint8") * 255
            # Creating the Final output mask
            output_msk = cv2.bitwise_or(output_msk, componentMask)
            area_cnt+= area
    
    if old_msk==[]:
        old_msk = output_msk
        continue
    
    flow = cv2.calcOpticalFlowFarneback(old_msk.astype(numpy.uint8)*255, output_msk.astype(numpy.uint8)*255, None, 0.5, 3, 7, 3, 5, 1.2, 0)
    old_msk = output_msk
    area_cnt_tot[frame_cnt] = area_cnt 

    cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    # cv2.putText(frame, str(analysis[0]-1), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    cv2.putText(frame, str(area_cnt), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', output_msk)

    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv = numpy.zeros_like(frame, dtype=numpy.float32)
    hsv[..., 1] = 255
    hsv[..., 0] = ((ang*180/numpy.pi/2)//45)*45.0
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow('Optical Flow', bgr)
    
    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
cv2.destroyAllWindows()

res = [x for x in area_cnt_tot if not(x==[])]
with open(r'/Users/matthieu/.ssh/ssh_to_graz/wdd_beetle_testvideos/Experiments_processing/test.txt', 'w') as fp:
    for item in res:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')