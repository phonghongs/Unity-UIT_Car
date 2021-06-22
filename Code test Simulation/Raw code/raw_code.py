import base64
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import cv2
from threading import Lock, Thread
from PIL import Image
from flask import Flask
from io import BytesIO
#------------- Add library ------------#
import time
#--------------------------------------#

def nothing(x):
   pass

global pre, original_Image, sendBack_angle, sendBack_Speed
sendBack_angle = 0
sendBack_Speed = 0
original_Image = []
pre = time.time()

lock = Lock()

#initialize our server
sio = socketio.Server()
#our flask (web) app
app = Flask(__name__)
#registering event handler for the server
@sio.on('telemetry')
def telemetry(sid, data):
    global sendBack_angle, sendBack_Speed, pre, original_Image
    if data:

        steering_angle = 0  #Góc lái hiện tại của xe
        speed = 0           #Vận tốc hiện tại của xe
        image = 0           #Ảnh gốc

        steering_angle = float(data["steering_angle"])
        speed = float(data["speed"])
        #Original Image
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        image = np.asarray(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        with lock:
            original_Image = np.copy(image)

        """
        - Chương trình đưa cho bạn 3 giá trị đầu vào:
            * steering_angle: góc lái hiện tại của xe
            * speed: Tốc độ hiện tại của xe
            * image: hình ảnh trả về từ xe
        
        - Bạn phải dựa vào 3 giá trị đầu vào này để tính toán và gửi lại góc lái và tốc độ xe cho phần mềm mô phỏng:
            * Lệnh điều khiển: send_control(sendBack_angle, sendBack_Speed)
            Trong đó:
                + sendBack_angle (góc điều khiển): [-25, 25]  NOTE: ( âm là góc trái, dương là góc phải)
                + sendBack_Speed (tốc độ điều khiển): [-150, 150] NOTE: (âm là lùi, dương là tiến)
        """

        print(1/(time.time() - pre))
        pre = time.time()
        send_control(sendBack_angle, sendBack_Speed)

    else:
        sio.emit('manual', data={}, skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__(),
        },
        skip_sid=True)


def main():
    global original_Image
    image =  0

    while True:
        with lock:
            image = np.copy(original_Image)
        try:
            cv2.imshow("image", image)
            print(image.shape)
        except:
            print("EEE")
        if cv2.waitKey(1) == 27:
            break


if __name__ == '__main__':
    #-----------------------------------  Setup  ------------------------------------------#
    thread_Main = Thread(target=main, args=())
    thread_Main.start()
    #--------------------------------------------------------------------------------------#
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)