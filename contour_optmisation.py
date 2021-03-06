# author : Safwene Ladhari
# The purpose of this module is to create an api to manipulate the Kinect Sensor
#
#
import numpy as np
import cv2
from freenect import sync_get_video as get_video
fgbg = cv2.createBackgroundSubtractorMOG2()


def center_detect():
    result = []
    (rgb, _) = get_video()
    orig = np.array(rgb[::1, ::1, ::-1])
    fgmask = fgbg.apply(orig)
    cv2.imshow('backgrondeliminated', fgmask)
    ret, thresh = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=1)
    im2, contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    index = 0
    for cnt in contours:
        if(cv2.arcLength(cnt, True)<250):
            contours.pop(index)
        else:
            index += 1
            hull = cv2.convexHull(cnt)
            M = cv2.moments(cnt)
            if(M['m00']!=0):
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                result.append([cx,cy])
    return(result)
#print(center_detect())
