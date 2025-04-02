import cv2
import numpy as np 
img = cv2.imread('C:\\Users\\paco1\\OneDrive\\Escritorio\\prueba.jpg')
imgn = np.zeros(img.shape[2], np.uint8)
print(img.shape)
b,g,r = cv2.split(img)
imgb = cv2.merge([b, imgn, imgn])
imgg = cv2.merge([imgn, g, imgn])
imgr = cv2.merge([imgn, imgn, r])

cv2.imshow('salidab', imgb)
cv2.imshow('salidag', imgg)
cv2.imshow('salidar', imgr)

cv2.waitKey(0)
cv2.destroyAllWindows()