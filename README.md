# Phần mềm mô phỏng xe tự hành - UIT_CAR_RACING - UNITY

Phầm mềm được sử dụng chính thức trong cuộc thi UIT CAR RACING - 2020
Thông tin cuộc thi: [here](http://ceday.uit.edu.vn/ceday/uit-car-racing-2020/?fbclid=IwAR09FrAJgNRWWauq4JIuBIAEvBnNb4IIprtKQhE-fD8wNqYuDayKKR4d5Bw)

# Cài đặt phần mềm mô phỏng

Link tải map: [here](https://drive.google.com/drive/folders/1dxIH1mCjbuDAfMuaFIBFVka7kUac-_ce?usp=sharing)

Các bạn tải map về và giải nén sẽ thu đc 2 folder:
* Folder Windows: dùng cho các bạn sử dụng nền tảng window, chạy file [tên map].exe (vd: 3D_MAP1-V2.exe)
* Folder Linux: dùng cho các bạn sử dụng nền tảng Linux (Khuyến nghị: Ubuntu 18.04), chạy file [tên map].x86_64 (vd: Map_1.x86_64)
    + Trước khi chạy file mô phỏng trên linux, các bạn bấm chuột phải vào file thực thi -> Properties -> Permissions -> tick vào ô Execute: Allow executing file as program

# Cài đặt các thư viện bắt buộc - Python

## Phần mềm mô phỏng cuộc thi UIT CAR RACING sử dụng phương thức giao tiếp Socket-Io 
## Để giao tiếp với phần mềm mô phỏng btc sử dụng ngôn ngữ Python (Đối với các đội sử dụng ngôn ngữ khác để giao tiếp với phần mềm mô phỏng, btc không có trách nhiệm hỗ trợ)

* [python-socketio](https://pypi.org/project/python-socketio/)
* [flask](https://pypi.org/project/Flask/)
* [OpenCv](https://opencv.org/)
* [eventlet](https://pypi.org/project/eventlet/)
* [Pillow](https://pypi.org/project/Pillow/)
* Code giao tiếp với phần mềm mô phỏng: 

```
git clone https://github.com/phonghongs/Unity-UIT_Car.git
```

# Hướng dẫn sử dụng

Sau khi cài đặt các thư viện cần thiết và có code giao tiếp vừa clone từ link git ở trên, ta bắt đầu vào chi tiết code

Cấu trúc Folder:    Code test Simulation|

                        --------------------|My code|

                                                -------|drive.py

                                                -------|model-010.h5

                                                -------|utils.py

                        --------------------|Raw code|
                        
                                                -------|raw_code.py

* My code: là folder chưa code mẫu của btc làm ví dụ cho các bạn biết cách sử dụng của code và làm sao để giao tiếp với phần mềm mô phỏng
```
python driver.py model-010.h5
```

* Raw code: Code này chứa mẫu giao tiếp với phần mềm mô phỏng, các đội nên code vào những phần mà đã gợi ý dưới đây
    + Phần "Add library": Nếu các bạn sử dụng thêm những thư viện khác thì có thể import từ phần này

    + Phần "Work space": Phần này sẽ chưa code xử lý chính của thí sinh, chương trình sẽ trả về những biến dưới đây sau mỗi lần request tới phần mềm mô phòng:
        - steering_angle: Góc lái hiện tại của xe
        - speed: Vận tốc hiện tại của xe
        - image: hình ảnh thu về từ xe
    + Các bạn dựa vào những biến này để xử lý và đưa ra tốc độ và góc chạy mà xe cần thực hiện. Sau khi đã xử lý xong, các bạn gán góc và tốc độ mong muốn vào 2 biến sau để gửi về phần mềm giả lập:
        - sendBack_angle (góc điều khiển): [-25, 25]  NOTE: (âm là góc trái, dương là góc phải)
        - sendBack_Speed (tốc độ điều khiển): [-150, 150] NOTE: (âm là lùi, dương là tiến)

    + Phần Setup: Khi bắt đầu chạy, chương trình sẽ bắt đầu chạy phần Setup này đầu tiên (chạy qua 1 lần), đây là phần mà các bạn setup các thông số trước khi chạy code chính như: Load model, thiết lập các biến cục bộ ...

# Kết thúc

Trước khi dừng phần mềm mô phỏng, các bạn nên dừng code giao tiếp với nó trước rồi mới tắt để tránh trường hợp phát sinh ra lỗi

## Chúc các bạn hoàn thành tốt lượt thi của mình

## Authors

* **Ly Hong Phong** - *Develope and Operation* - [phonghongs](https://github.com/phonghongs)

* **Che Quang Huy** - *Develope and Operation* - [chequanghuy](https://github.com/chequanghuy)

## License
