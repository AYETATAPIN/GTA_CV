import numpy as np
import cv2 as cv
import argparse

# parser = argparse.ArgumentParser(description='This sample demonstrates the meanshift algorithm. \
#                                               The example file can be downloaded from: \
#                                               https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
# parser.add_argument('image', type=str, help='path to image file')
# args = parser.parse_args()
cap = cv.VideoCapture(0)
# берем первый кадр с видео
ret,frame = cap.read()
frame = cv.resize(frame, (1900, 1000))

# устанавливаем изначальное окно
x, y, w, h = 1000, 400, 400, 500 # просто подбор значений
track_window = (x, y, w, h)

# устанавливаем регионы интереса (ROI) для отслеживания
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# устанавливаем критерий завершения, либо 10 итераций либо свдиг хотя бы на 1 пиксель
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

while 1:
    ret, frame = cap.read()
    frame = cv.resize(frame, (1900, 1000))
    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        # применяем Meanshift к новой области
        ret, track_window = cv.meanShift(dst, track_window, term_crit)
        # Рисуем его на картинке
        x,y,w,h = track_window
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv.imshow('img2',img2)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break