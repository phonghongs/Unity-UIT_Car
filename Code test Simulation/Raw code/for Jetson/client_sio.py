import base64
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import cv2
import threading
import time
from PIL import Image
from flask import Flask
from io import BytesIO
from threading import Thread

sio = socketio.Client()
global IMAGE
IMAGE = []
lock = threading.Lock()
pre_time = 0


@sio.event
def connect():
    print('connection established')

@sio.on('feedback')
def feedback(data):
    global IMAGE, pre_time
    print(1/(time.time() - pre_time))
    try:
        with lock:
            IMAGE = Image.open(BytesIO(base64.b64decode(data['image'])))
            IMAGE = np.asarray(IMAGE)
            IMAGE = cv2.cvtColor(IMAGE, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(e)
    pre_time = time.time()
    sio.emit('telemetry', {'mode' : '1', 'steering' : '2', 'speed': '0'})
    
@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:4567')

while True:
    try:
        with lock:
            cv2.imshow("IMAGES", IMAGE)
    except:
        print("cannot show image")

    if cv2.waitKey(1) == ord("q"):
        sio.disconnect()
        break