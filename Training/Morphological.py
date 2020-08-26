import cv2
import numpy as np

img = cv2.imread('imgs/RGB.png', 0)


kernel = np.ones((5,5), np.uint8)
erosion = cv2.erode(img,kernel,iterations = 1)
dilation = cv2.dilate(img,kernel,iterations = 1)
cv2.dilate(img, kernel)

cv2.imshow('img', img)
cv2.imshow('erosion', erosion)
cv2.imshow('dilation', dilation)

cv2.waitKey(0)
