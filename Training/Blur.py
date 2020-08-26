import cv2
import numpy as np

img = cv2.imread('imgs/RGB.png', 0)

blur = cv2.blur(img,(5,5))
laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

cv2.imshow('img', img)
cv2.imshow('blur', blur)
cv2.imshow('laplacian', laplacian)
cv2.imshow('sobelx', sobelx)
cv2.imshow('sobely', sobely)

cv2.waitKey(0)