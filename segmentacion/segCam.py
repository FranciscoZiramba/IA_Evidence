#====================SIN SEGMENTACIÓN DE COLORES====================
"""
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0) # 0 es como un broadcast para que encuentre la cámara
# Es decir que se pueden usar más de una cámara

while True:
    ret, img = cap.read()
    if(ret):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        cv.imshow('salida',img)
    k = cv.waitKey(1) & 0xFF # Se espera un segundo para cerrar la ventana
    if k == 27 :
        break
cap.release() # Se libera la cámara y buffer
cv.destroyAllWindows() # Se cierran todas las ventanas
"""
#====================CON SEGMENTACIÓN DE COLORES====================
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0) # 0 es como un broadcast para que encuentre la cámara
# Es decir que se pueden usar más de una cámara

while True:
    ret, img = cap.read()
    if(ret):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        ub = np.array([35, 40, 40])
        ua = np.array([85, 255, 255])
        mask = cv.inRange(hsv, ub, ua)
        res = cv.bitwise_and(img, img, mask=mask)

        cv.imshow('res', res)
        #cv.imshow('gray', gris)

        k = cv.waitKey(1) & 0xFF # Se espera un segundo para cerrar la ventana
        if k == 27 :
            break
cap.release() # Se libera la cámara y buffer
cv.destroyAllWindows() # Se cierran todas las ventanas