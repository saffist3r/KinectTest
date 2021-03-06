import numpy as np
import cv2
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

from cv2 import waitKey

global rgb, initdepth
global BM,GM,RM,BMM,GMM,RMM
BM = 0
GM = 0
RM = 180
BMM = 255
GMM = 255
RMM = 2
def change_BM(value):
    global BM
    BM = value


def change_GM(value):
    global GM
    GM = value


def change_RM(value):
    global RM
    RM = value


def change_BMM(value):
    global BMM
    BMM = value


def change_GMM(value):
    global GMM
    GMM = value


def change_RMM(value):
    global RMM
    RMM = value


def nothing(x):
    global BM, GM, RM, BMM, GMM, RMM
    file = open('config.txt', 'w')
    file.write(str(BM)+'\n')
    file.write(str(GM)+'\n')
    file.write(str(RM)+'\n')
    file.write(str(BMM)+'\n')
    file.write(str(GMM)+'\n')
    file.write(str(RMM)+'\n')
    print('Closing Config Window')
    #cv2.destroyWindow('1')

def mainfunc():
    lower_red = np.array([0, 0, 69])
    upper_red = np.array([255, 255, 255])
    global rgb, initdepth
    global BM, GM, RM, BMM, GMM, RMM
    BM = 0
    GM = 0
    RM = 180
    BMM = 255
    GMM = 255
    RMM = 255
    (dst, _) = get_video()
    #-----------
    orig = np.array(dst[::1, ::1, ::-1])
    frame = np.array(dst[::1, ::1, ::-1])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([BM, GM, RM])
    upper_red = np.array([BMM, GMM, RMM])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    dst = cv2.bitwise_and(frame, frame, mask=mask)
    #-----------
    kernel = np.ones((5, 5), np.float32) / 25
    rgb = cv2.filter2D(dst, -1, kernel)
    gray_image = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_SIMPLEX
    index = 0
    for cnt in contours:
        epsilon = 0.15 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if cv2.arcLength(approx, True) < 20:
            contours.pop(index)
        else:
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
                index = index + 1
                #cv2.drawContours(rgb, approx, -1, (0, 255, 0), 3)
    cv2.namedWindow('rgb')
    cv2.startWindowThread()
    cv2.createTrackbar('BMin', 'rgb', BM, 255, change_BM)
    cv2.createTrackbar('GMin', 'rgb', GM, 255, change_GM)
    cv2.createTrackbar('RMin', 'rgb', RM, 255, change_RM)
    cv2.createTrackbar('BMax', 'rgb', BMM, 255, change_BMM)
    cv2.createTrackbar('GMax', 'rgb', GMM, 255, change_GMM)
    cv2.createTrackbar('RMax', 'rgb', RMM, 255, change_RMM)
    cv2.createTrackbar('0 : OFF \n1 : ON', 'rgb', 0, 1, nothing)
    while(1):
        (dst, _) = get_video()
        # -----------
        frame = np.array(dst[::1, ::1, ::-1])
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array([BM, GM, RM])
        upper_red = np.array([BMM, GMM, RMM])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        dst = cv2.bitwise_and(frame, frame, mask=mask)
        # -----------
        kernel = np.ones((5, 5), np.float32) / 25
        rgb = cv2.filter2D(dst, -1, kernel)
        gray_image = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        index = 0
        for cnt in contours:
            epsilon = 0.15 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if cv2.arcLength(approx, True) < 20:
                contours.pop(index)
            else:
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    index = index + 1
        cv2.imshow('rgb',rgb)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break



