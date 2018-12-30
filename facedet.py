#!/usr/bin/env python
# -*- coding: utf-8 -*-

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, time

# frame size
FRAME_W = 320
FRAME_H = 192

cascPath = './lbpcascade_frontalface.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

camera = PiCamera()
camera.resolution = (FRAME_W, FRAME_H)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(FRAME_W, FRAME_H))
time.sleep(0.1)

for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    frame = image.array

    # greyscale convert
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # face detect
    faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))

    # draw frame
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    frame = cv2.resize(frame, (540,300))

    # display 
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break

cv2.destroyAllWindows()
