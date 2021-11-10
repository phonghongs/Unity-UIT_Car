
# Import socket module
import socket
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
        message_getState = bytes("0", "utf-8")
        s.sendall(message_getState)
        state_date = s.recv(100)
        current_speed, current_angle = state_date.decode("utf-8").split(' ')

        message = bytes(f"1 {sendBack_angle} {sendBack_Speed}", "utf-8")
        s.sendall(message)
        data = s.recv(100000)

        """
        - Chương trình đưa cho bạn 1 giá trị đầu vào:
            * image: hình ảnh trả về từ xe
            * current_speed: vận tốc hiện tại của xe
            * current_angle: góc bẻ lái hiện tại của xe

        - Bạn phải dựa vào giá trị đầu vào này để tính toán và gán lại góc lái và tốc độ xe vào 2 biến:
            * Biến điều khiển: sendBack_angle, sendBack_Speed
            Trong đó:
                + sendBack_angle (góc điều khiển): [-25, 25]  NOTE: ( âm là góc trái, dương là góc phải)
                + sendBack_Speed (tốc độ điều khiển): [-150, 150] NOTE: (âm là lùi, dương là tiến)
        """

        try:
            image = cv2.imdecode(np.frombuffer(data, np.uint8), -1)

            print(current_speed, current_angle)
            print(image.shape)
            # your process here

            sendBack_angle = 0
            sendBack_Speed = 0

        except Exception as er:
            print(er)
            pass
finally:
    print('closing socket')
    s.close()
