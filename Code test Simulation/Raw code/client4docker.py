
# Import socket module 
import socket       
import sys      
import time
import cv2
import numpy as np


# Create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Define the port on which you want to connect 
port = 54321                
  
# connect to the server on local computer 
s.connect(('host.docker.internal', port)) 

pre = time.time()

angle = 50
speed = 100

try:
    while True:
        # Send data
        print(angle, speed)
        message = bytes(f"{angle} {speed}", "utf-8")
        s.sendall(message)

        data = s.recv(60000)
        # print(data)
        try:
            decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
            print(decoded.shape)
        except Exception as er:
            print(er)
            pass
        # cv2.imshow("IMG", decoded)
        # key = cv2.waitKey(1)

        print(1/(time.time() - pre))
        pre = time.time()

finally:
    print('closing socket')
    s.close()