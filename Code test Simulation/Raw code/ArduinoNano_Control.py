from full_pipeline import *
import time
import numpy as np
import cv2


from moviepy.editor import VideoFileClip
from IPython.display import HTML
from imutils.video import VideoStream

CENTER = 45
MAXSPEED = 20
RESETLANE = False
but_pin = 35

# cv2.namedWindow("Control")
# cv2.createTrackbar("Min H", "Control", 33, 255, nothing)
# cv2.createTrackbar("Min S", "Control", 50, 255, nothing)
# cv2.createTrackbar("Min V", "Control", 62, 255, nothing)

# cv2.createTrackbar("Max H", "Control", 102, 255, nothing)
# cv2.createTrackbar("Max S", "Control", 255, 255, nothing)
# cv2.createTrackbar("Max V", "Control", 248, 255, nothing)


def gstreamer_pipeline(
    capture_width=640,
    capture_height=480,
    display_width=640,
    display_height=480,
    framerate=20,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def blink(channel):
    print("Reset Lane")
    RESETLANE = True


def main():
    global RESETLANE, kI2Caddress, bus, CENTER, MAXSPEED, RESETLANE, but_pin

    vs = cv2.VideoCapture("VID_20200912_192752_810_Trim.mp4")
    time.sleep(2)
    # Grab location of calibration images
    cal_image_loc = glob.glob('camera_cal/*.jpg')
        # Calibrate camera and return calibration data
    lanes = LANE_DETECTION()

    # window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)


    while True:
        _, img = vs.read()
        # _, img = cap.read()

        # MiH = cv2.getTrackbarPos("Min H", "Control")
        # MiS = cv2.getTrackbarPos("Min S", "Control")
        # MiV = cv2.getTrackbarPos("Min V", "Control")

        # MaH = cv2.getTrackbarPos("Max H", "Control")
        # MaS = cv2.getTrackbarPos("Max S", "Control")
        # MaV = cv2.getTrackbarPos("Max V", "Control")
        

        # min_HSV = np.array([MiH, MiS, MiV])
        # max_HSV = np.array([MaH, MaS, MaH])

        if RESETLANE:
            RESETLANE = False
            print("reset")

        min_HSV = np.array([86, 98, 135])
        max_HSV = np.array([255, 208, 255])

        img = cv2.resize(img, (640, 480))
        angle = 45
        
        cv2.imshow("imgss", img)
        try:
            result = lanes.draw_lines(img)
            cv2.imshow("result s", result)

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            pass

            # This also acts as
        keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
        if keyCode == 27:
            break

    vs.release()
    # cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()