#!/usr/bin/env python
# -*- coding: utf-8 -*-

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, time

import gmail
import os

username = 'XXX@gmail.com'
password = 'YYYYYY'

client = gmail.GMail(username, password)

body_html = u"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Face Detected.</title>
  </head>
  <body>
    <h1>Face Detect.</h1>
  </body>
</html>
"""

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

    facedet = 0

    # greyscale convert
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # face detect
    faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))

    # draw frame
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print('detect face x,y = %d,%d [%dx%d]' % (x, y, w, h));
        cv2.imwrite('zerow.jpg', frame)
        facedet = 1

    # frame = cv2.resize(frame, (540,300))

    # if face detect, send email
    if facedet == 1:
        time.sleep(1)
        message = gmail.Message(u'ZeroW Face', to=username, html=body_html, attachments=['zerow.jpg'])
        client.send(message)
        client.close()
        print('Send Mail.')
        facedet = 0
        time.sleep(10)

    # display 
    #cv2.imshow('Video', frame)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break

cv2.destroyAllWindows()
