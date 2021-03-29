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


sio = socketio.Server()
app = Flask(__name__)
global IMG, readC, lock, currentSpeed, b64_code, cap
cap = cv2.VideoCapture(0)

b64_code = ""
lock = threading.Lock()
readC = True


def ReadCamera(cap, lock):
    global IMG, readC
    while readC:
        try:
            with lock:
                _, IMG = cap.read()
        except:
            print("Cannot read camera")
    cap.release()

def UpdateSpeed():
    global currentSpeed
    while readC:
        currentSpeed = 50


def send_feedback(_image, _currentSpeed):
    sio.emit(
        "feedback",
        data={
            'image': _image,
            'currentSpeed': _currentSpeed.__str__(),
        },
        skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_feedback(5, 5)

@sio.on('telemetry')
def telemetry(sid, data):
    global lock, IMG, currentSpeed, b64_code, cap
    currentSpeed = 0
    if data:
        try:
            _whatMode = int(data['mode'])
            _steering = int(data['steering'])
            _speed = int(data['speed'])
            print(_whatMode, _steering, _speed)
        except Exception as e:
            print(e)

        try:
            img_str = cv2.imencode('.jpg', IMG)[1].tostring()
            b64_code = base64.b64encode(img_str)
        except Exception as e:
            print(e)
        
        send_feedback(b64_code, currentSpeed)

if __name__ == '__main__':
    #-----------------------------------  Setup  ------------------------------------------#
    readCamera_Thread = Thread(target=ReadCamera, args=(cap, lock))
    readCamera_Thread.start()

    #--------------------------------------------------------------------------------------#
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)