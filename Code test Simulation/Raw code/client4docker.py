
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

sendBack_angle = 0
sendBack_Speed = 0

try:
    while True:
        # Send data
        message = bytes(f"{sendBack_angle} {sendBack_Speed}", "utf-8")
        s.sendall(message)

        data = s.recv(1000000)
        try:
            image = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
        except Exception as er:
            print(er)
            pass

        """
        - Chương trình đưa cho bạn 1 giá trị đầu vào:
            * image: hình ảnh trả về từ xe
        
        - Bạn phải dựa vào giá trị đầu vào này để tính toán và gán lại góc lái và tốc độ xe vào 2 biến:
            * Biến điều khiển: sendBack_angle, sendBack_Speed
            Trong đó:
                + sendBack_angle (góc điều khiển): [-25, 25]  NOTE: ( âm là góc trái, dương là góc phải)
                + sendBack_Speed (tốc độ điều khiển): [-150, 150] NOTE: (âm là lùi, dương là tiến)
        """

        # your process here

        sendBack_angle = 0
        sendBack_Speed = 0

finally:
    print('closing socket')
    s.close()