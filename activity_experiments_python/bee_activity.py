import numpy
import cv2
import os 

import matplotlib
import matplotlib.pyplot
import matplotlib.patches

# VIDEO CREATION
def video_generation(images_list, video_folder='./', video_name='test_vid.mp4', fps=30):
    print('Saving video results in ' + video_folder + video_name)
    
    if (video_name in os.listdir(video_folder)):
        os.system('rm {}'.format(video_folder+video_name))
        
    height, width = images_list[0].shape[:2]
    
    # video = cv2.VideoWriter(video_folder+video_name, cv2.VideoWriter_fourcc('a','v','c','1'), fps, (width,height))
    video = cv2.VideoWriter(video_folder+video_name, cv2.VideoWriter_fourcc('m','p','4','v'), fps, (width,height))
    #video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('X','V','I','D'), fps, (width,height))
    
    for i in range(0, len(images_list)):
        if (len(images_list[i].shape) == 3):
            video.write(numpy.uint8(images_list[i][:,:,[2,1,0]]))
        else :
            video.write(numpy.uint8(images_list[i]))

    cv2.destroyAllWindows()
    video.release()
    del video

def compute_video_activity(video, threshold=15, cropX=None, cropY=None, frames='all', video_save=False, video_filename=None, video_foldername=None):
    
    cap = cv2.VideoCapture(video)
    
    prev_frame = numpy.array([])
    activities = numpy.zeros(2000000)

    if video_save:
        vid = [[]]*20000
    
    if frames=='all':
        stop_frame=2000000000
    else :
        stop_frame=frames
        
    frame_count = 0
    print('')
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_count += 1
        if ret == False or frame_count > stop_frame:
            print('')
            break
        
        if not(cropX is None):
            frame_crop = frame[cropX[0]:cropX[1],:]
        else:
            frame_crop=frame
        if not(cropY is None):
            frame_crop = frame_crop[:,cropY[0]:cropY[1]]
        
        mean_frame = numpy.mean(frame_crop, axis=2).astype('uint8')
        gauss_frame = cv2.GaussianBlur(mean_frame, (11,11), 1)
        # equal_frame = cv2.equalizeHist(gauss_frame)
        res_frame = gauss_frame.astype('float')
             
        print('\r'+str(frame_count) + ' frames processed     ', sep=' ', end='', flush=True)
        
        if frame_count == 1:
            prev_frame = res_frame
            continue
        
        
        act = numpy.abs(res_frame-prev_frame) >= threshold
        
        activity = numpy.sum(act)
        activity = activity/(res_frame.shape[0]*res_frame.shape[1])
        activities[frame_count-1] = activity
        prev_frame = res_frame

        if video_save :
            vid[frame_count-1] = frame_crop
            vid[frame_count-1][:,:,0]=numpy.maximum(vid[frame_count-1][:,:,0], numpy.uint8(act)*255)

    if video_save:
        vid = [v for v in vid if not(v==[])]
        video_generation(vid, video_folder=video_foldername, video_name=video_filename, fps=30)
    
    return list(activities[:(frame_count-2)])


def compute_video_intensity(video, cropX=None, cropY=None, frames='all'):
    
    cap = cv2.VideoCapture(video)
    
    intensities = numpy.zeros(200000)
    
    if frames=='all':
        stop_frame=2000000000
    else :
        stop_frame=frames
        
    frame_count = 0
    print('')
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_count += 1
        if ret == False or frame_count > stop_frame:
            print('')
            break
        
        if not(cropX is None):
            frame_crop = frame[cropX[0]:cropX[1],:]
        else:
            frame_crop=frame
        if not(cropY is None):
            frame_crop = frame_crop[:,cropY[0]:cropY[1]]
        
        mean_frame = numpy.mean(frame_crop, axis=2).astype('uint8')
        gauss_frame = cv2.GaussianBlur(mean_frame, (11,11), 1)
        # equal_frame = cv2.equalizeHist(gauss_frame)
        res_frame = gauss_frame.astype('float')
             
        print('\r'+str(frame_count) + ' frames processed     ', sep=' ', end='', flush=True)
        
        intensity = numpy.sum(res_frame)
        intensity = intensity/(res_frame.shape[0]*res_frame.shape[1])
        intensities[frame_count-1] = intensity
    return list(intensities[:(frame_count-2)])

def show_video_frame(video, cropX=None, cropY=None, frame_of_interest=0, figfilename=None):

    cap = cv2.VideoCapture(video)
    
    frame_count = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_count += 1
        if ret == False or frame_count > frame_of_interest:
            xy = [0,0]
            width = 0
            height = 0
            if not(cropX is None):
                frame_crop = frame[cropX[0]:cropX[1],:]
                xy[1]=cropX[0]
                height = cropX[1]-cropX[0]
            else:
                frame_crop=frame
            if not(cropY is None):
                frame_crop = frame_crop[:,cropY[0]:cropY[1]]
                xy[0]=cropY[0]
                width = cropY[1]-cropY[0]
                
            rectpatch = matplotlib.patches.Rectangle(xy, width, height, color='r', alpha=0.3)
            
            mean_frame = numpy.mean(frame_crop, axis=2).astype('uint8')
            gauss_frame = cv2.GaussianBlur(mean_frame, (11,11), 1)
            equal_frame = cv2.equalizeHist(gauss_frame)
            res_frame = equal_frame.astype('float')

            fig, ax = matplotlib.pyplot.subplots(2, 3, figsize=(12,6))
            ax[0,0].imshow(frame)
            ax[0,0].add_patch(rectpatch)
            ax[0,1].imshow(frame_crop)
            ax[0,2].imshow(mean_frame)
            ax[1,0].imshow(gauss_frame)
            ax[1,1].imshow(equal_frame)
            ax[1,2].imshow(res_frame)
            fig.tight_layout()
            if not(figfilename==None):
                matplotlib.pyplot.savefig(figfilename)
            break