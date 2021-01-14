import cv2
import numpy as np

img = cv2.imread('imgs/RGB.png', 0)


t1 = 50
t2 = 100
t3 = 150
ret1, thresh1 = cv2.threshold(img,t1,255,cv2.THRESH_BINARY)
ret2, thresh2 = cv2.threshold(img,t2,255,cv2.THRESH_BINARY)
ret3, thresh3 = cv2.threshold(img,t3,255,cv2.THRESH_BINARY)

thresh4 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
thresh5 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


cv2.imshow('thresh1', thresh1)
cv2.imshow('thresh2', thresh2)
cv2.imshow('thresh3', thresh3)
cv2.imshow('thresh4', thresh4)
cv2.imshow('thresh5', thresh5)

cv2.waitKey(0)