#import cv2
#img = cv2.imread('C:\Users\paco1\OneDrive\Imagenes\Screenshots\prueba.jgp',1) # Para cargar la imagen es importante la direccion C://
#cv2.imshow('salida', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

import cv2
img = cv2.imread("C:\\Users\\paco1\\OneDrive\\Escritorio\\prueba.jpg") # Para cargar la imagen es importante la direccion C://
cv2.imshow('salida', img)
#quitar color
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img3 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img4 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('salida2', img2)
cv2.imshow('salida3', img3)
cv2.imshow('salida4', img4)

cv2.waitKey(0)
cv2.destroyAllWindows()