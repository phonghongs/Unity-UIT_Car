import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('imgs/RGB.png', 0)


histr = cv2.calcHist([img], [0],None,[256],[0,256]) 

equ = cv2.equalizeHist(img)

res = np.hstack((img,equ))
cv2.imshow('res', res)

plt.plot(histr)
plt.show()