me, (10, 2), (100,20), (255,255,255), -1)
    # cv2.putText(frame, str(analysis[0]-1), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    cv2.putText(frame, str(area_cnt), (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', output_msk)
    
    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
cv2.destroyAllWindows()