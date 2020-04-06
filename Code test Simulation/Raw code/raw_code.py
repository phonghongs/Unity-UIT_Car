import base64
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import cv2
from PIL import Image
from flask import Flask
from io import BytesIO
#------------- Add library ------------#

from keras.models import load_model
import argparse
import utils

#--------------------------------------#

takeDepth = False      #Có lấy ảnh depth về ko ?

#initialize our server
sio = socketio.Server()
#our flask (web) app
app = Flask(__name__)
#registering event handler for the server
@sio.on('telemetry')
def telemetry(sid, data):
    if data:

        steering_angle = 0  #Góc lái hiện tại của xe
        speed = 0           #Vận tốc hiện tại của xe
        image = 0           #Ảnh gốc
        depth_image = 0     #Ảnh Depth


        if takeDepth:
            steering_angle = float(data["steering_angle"])
            speed = float(data["speed"])
            #Original Image
            image = Image.open(BytesIO(base64.b64decode(data["image"])))
            image = np.asarray(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #DepthImage 
            depth_image = Image.open(BytesIO(base64.b64decode(data["depth_image"])))   
            depth_image = np.asarray(depth_image) 
        else:
            steering_angle = float(data["steering_angle"])
            speed = float(data["speed"])
            #Original Image
            image = Image.open(BytesIO(base64.b64decode(data["image"])))
            image = np.asarray(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        """
        - Chương trình đưa cho bạn 3 giá trị đầu vào:
            * steering_angle: góc lái hiện tại của xe
            * speed: Tốc độ hiện tại của xe
            * image: hình ảnh trả về từ xe
            * depth_image: ảnh chiều sâu được xe trả về (xét takeDepth = True, ảnh depth sẽ được trả về sau khi 'send_control' được gửi đi)
        
        - Bạn phải dựa vào 3 giá trị đầu vào này để tính toán và gửi lại góc lái và tốc độ xe cho phần mềm mô phỏng:
            * Lệnh điều khiển: send_control(sendBack_angle, sendBack_Speed)
            Trong đó:
                + sendBack_angle (góc điều khiển): [-25, 25]  NOTE: ( âm là góc trái, dương là góc phải)
                + sendBack_Speed (tốc độ điều khiển): [-150, 150] NOTE: (âm là lùi, dương là tiến)
        """
        sendBack_angle = 0
        sendBack_Speed = 0
        try:
            #------------------------------------------  Work space  ----------------------------------------------#


            cv2.waitKey(1)

            #------------------------------------------------------------------------------------------------------#
            print('{} : {}'.format(sendBack_angle, sendBack_Speed))
            send_control(sendBack_angle, sendBack_Speed, takeDepth)
        except Exception as e:
            print(e)
    else:
        sio.emit('manual', data={}, skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0, takeDepth)


def send_control(steering_angle, throttle, takeDepth):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__(),
            'takeDepth': takeDepth.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    
    #-----------------------------------  Setup  ------------------------------------------#
    


    #--------------------------------------------------------------------------------------#
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
    