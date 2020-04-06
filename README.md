# Unity-UIT_Car

UIT Car simulation - Socket io

This Car simulation project uses Unity 2019.3

# Getting Started

```
git clone https://github.com/phonghongs/Unity-UIT_Car.git
```

## Prerequisites


Install [Tensorflow](https://pypi.org/project/tensorflow/)

```
pip3 install tensorflow
```

Install [Keras](https://pypi.org/project/Keras/)

```
pip3 install Keras
```

## Running the tests

### Run Car simulation

In Final Demo 1 - 2:

* For Windows: Run [ Test Socket V1.exe ]
* For Linux: Run [ demo.x86_64 ] (u much set permision for demo.x86_64)

----

### On simulator

* Start: Auto run map 1
* Option: Change Resolution, quality,...
* Quit: quit .-.

#### On map 1

* Just do anything u know to control the car :) it Ez, right ? :))

#### on map 2

* I gave you a signs map : [Signs System.PNG]. At each point, u had 15 signs to set up.

* Click: Signs Sys to open the Signs Setting table
    + Choose the point , Sign 1, Sign 2 .. etc
    + What Sign that u want to learn
    + Done to close Signs Setting table

### Code ? Ok :)

In folder [Code test Simulation] i gave u 2 code folder

* My code: as the name, we had the code using Deep learning to control the car. If u want to know more about this code, plz contact us.

```
python3 drive.py model-010.h5
```

* Raw code: We had write a Note into this code. Read it! .-.

    * u must have 3 space to write on this code:
        - Setup: read model, read argument etc ...
        - Work space: like it name .-. do everything u can on this space (using steering_angle, speed, image, depth_image)
        - Global Variable: after "Add library"...
     

## Authors

* **Ly Hong Phong** - *Develope and Operation* - [phonghongs](https://github.com/phonghongs)

* **Che Quang Huy** - *Develope and Operation* - [chequanghuy](https://github.com/chequanghuy)

## License
