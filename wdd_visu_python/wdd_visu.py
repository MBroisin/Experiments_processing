import cv2 
import matplotlib
import matplotlib.pyplot
import numpy


def show_video_frame_wdd(video, cropX=None, cropY=None, frame_of_interest=0, rotate=True):

    cap = cv2.VideoCapture(video)
    
    frame_count = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_count += 1
        if ret == False or frame_count > frame_of_interest:
            if rotate:
                frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_90_CLOCKWISE)
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
            break

def compute_video_intensity_wdd(video, cropX=None, cropY=None, frames='all', rotate=True):
    
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
        if rotate:
            frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_90_CLOCKWISE)

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

def compute_time_shift_wdd(ledmeasure, ledtheory, plot=True, save_plot_fname=None, fps=30):
    # print(datapack[key])
    ledint = numpy.array(ledmeasure)
    ledint = ledint-numpy.min(ledint)
    ledint = ledint/numpy.max(ledint)
    ledint = 1-(numpy.array(ledint)>0.5).astype(numpy.int8)
    ledtheory = numpy.array(ledtheory)
    ledtheory = ledtheory-numpy.min(ledtheory)
    ledtheory = ledtheory/numpy.max(ledtheory)
    ledtheory = 1-ledtheory
    time_shift = numpy.argmax(numpy.correlate(ledint, ledtheory,'valid'))

    if plot :
        fig = matplotlib.pyplot.figure(figsize=(12,5))
        matplotlib.pyplot.plot(numpy.array(range(ledint.shape[0]))/fps, ledint, 'g', label='Measurement')
        matplotlib.pyplot.plot(numpy.array(range(ledtheory.shape[0]))/fps, ledtheory, ':b', label='Theory')
        matplotlib.pyplot.plot((numpy.array(range(ledtheory.shape[0]))+time_shift)/fps, ledtheory, 'r', label='Theory_corrected')
        matplotlib.pyplot.legend()
        matplotlib.pyplot.title('LED visual intensity pattern and LED command pattern timing matching')
        matplotlib.pyplot.xlabel('Time [s]')
        matplotlib.pyplot.ylabel('Theoritical and observed LED intensity [-]')
        if not(save_plot_fname==None):
            matplotlib.pyplot.savefig(save_plot_fname)

    return time_shift