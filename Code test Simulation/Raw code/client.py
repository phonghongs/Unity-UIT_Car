# Import socket module
import socket
import cv2
from matplotlib import type1font
import numpy as np
import json

global typereturn
typereturn = 1
MODE_1 = 1
MODE_2 = 2
MODE_3 = 3
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
PORT = 11000
# connect to the server on local computer
s.connect(('127.0.0.1', PORT))

def jsonObject(cmd = 1, speed = 0, angle = 0):
    cmt = {}
    if cmd == 1:
        cmt['Cmd'] = cmd
        cmt['Speed'] = speed
        cmt['Angle'] = angle
    else:
        cmt['Cmd'] = cmd
    return bytes(str(cmt), "utf-8")

if __name__ == "__main__":
    try:
        while True:
            if typereturn == MODE_1:
                s.sendall(jsonObject(MODE_1, 2, 3))
                data = s.recv(255)
                y = json.loads(data)
                print(y)

            if typereturn == MODE_1:
                s.sendall(jsonObject(MODE_2))
                data = s.recv(100000)
                try:
                    image = cv2.imdecode(
                        np.frombuffer(
                            data,
                            np.uint8
                            ), -1
                        )
                except Exception as er:
                    print(er)
                    pass

                print(image.shape)
                cv2.imshow("IMG", image)

            if typereturn == MODE_1:
                s.sendall(jsonObject(MODE_3))
                data = s.recv(100000)
                try:
                    image = cv2.imdecode(
                        np.frombuffer(
                            data,
                            np.uint8
                            ), -1
                        )
                except Exception as er:
                    print(er)
                    pass

                print(image.shape)
                cv2.imshow("SEG", image)

            key = cv2.waitKey(1)
            if key == ord('n'):
                typereturn += 1
                if typereturn > MODE_1:
                    typereturn = 0
            elif key == ord('q'):
                break

    finally:
        print('closing socket')
        s.close()
