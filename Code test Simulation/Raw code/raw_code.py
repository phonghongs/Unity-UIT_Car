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
from full_pipeline import *

#--------------------------------------#

global lanes

def nothing(x):
   pass

# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("s_thresh_L", "Trackbars", 125, 255, nothing)
# cv2.createTrackbar("s_thresh_R", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("r_thresh_L", "Trackbars", 200, 255, nothing)
# cv2.createTrackbar("r_thresh_R", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("sx_thresh_L", "Trackbars", 10, 255, nothing)
# cv2.createTrackbar("sx_thresh_R", "Trackbars", 100, 255, nothing)

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
            # global lanes


            # sl = cv2.getTrackbarPos("s_thresh_L", "Trackbars")
            # sr = cv2.getTrackbarPos("s_thresh_R", "Trackbars")
            # rl = cv2.getTrackbarPos("r_thresh_L", "Trackbars")
            # rr = cv2.getTrackbarPos("r_thresh_R", "Trackbars")
            # sxl = cv2.getTrackbarPos("sx_thresh_L", "Trackbars")
            # sxr = cv2.getTrackbarPos("sx_thresh_R", "Trackbars")

            sl = 88
            sr = 116
            rl = 40
            rr = 255
            sxl = 56
            sxr = 127

            # sl = 11
            # sr = 80
            # rl = 191
            # rr = 201
            # sxl = 19
            # sxr = 113

            sobel_kernel = 3

            s_thresh = (sl, sr)
            R_thresh = (rl, rr)
            sx_thresh = (sxl, sxr)

            distorted_img = np.copy(image[:, :])

            # distorted_img = cv2.blur(distorted_img, (3, 3))

            cv2.imshow("original", distorted_img)
            # Pull R
            R = distorted_img[:,:,0]
            
            # Convert to HLS colorspace
            hls = cv2.cvtColor(distorted_img, cv2.COLOR_RGB2HLS).astype(np.float)
            h_channel = hls[:,:,0]
            l_channel = hls[:,:,1]
            s_channel = hls[:,:,2]
            
            # Sobelx - takes the derivate in x, absolute value, then rescale
            sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0, ksize = sobel_kernel)
            abs_sobelx = np.absolute(sobelx)
            scaled_sobelx = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
            
            # Threshold x gradient
            sxbinary = np.zeros_like(scaled_sobelx)
            sxbinary[(scaled_sobelx >= sx_thresh[0]) 
                    & (scaled_sobelx <= sx_thresh[1])] = 1

            # Threshold R color channel
            R_binary = np.zeros_like(R)
            R_binary[(R >= R_thresh[0]) & (R <= R_thresh[1])] = 1
            
            # Threshold color channel
            s_binary = np.zeros_like(s_channel)
            s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1


            combined_binarys = np.zeros_like(sxbinary)
            combined_binarys[((s_binary == 1) & (sxbinary == 1)) 
                            | ((sxbinary == 1) & (R_binary == 1))
                            | ((s_binary == 1) & (R_binary == 1))] = 255

            # kernel = np.ones((3,3), np.uint8)
            # erosion = cv2.erode(combined_binarys, kernel, iterations=1)
            # dilation = cv2.dilate(erosion, kernel, iterations=1)

            gray = cv2.cvtColor(distorted_img, cv2.COLOR_BGR2YUV)

            cv2.imshow("gray", gray)

            # result = lanes.draw_lines(image)
            cv2.imshow("result s", combined_binarys)

            cv2.waitKey(1)
            #------------------------------------------------------------------------------------------------------#
            print('{} : {}'.format(sendBack_angle, sendBack_Speed))
            send_control(sendBack_angle, sendBack_Speed)
        except Exception as e:
            print(e)
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


if __name__ == '__main__':
    
    #-----------------------------------  Setup  ------------------------------------------#
    global lanes

    # lanes = LANE_DETECTION()

    #--------------------------------------------------------------------------------------#
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)