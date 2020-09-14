import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
image = cv2.imread("pysource_qrcode.png")

while True:
    _, frame = cap.read()

    decodedObjects = pyzbar.decode(frame)
    decodedObjects1 = pyzbar.decode(image)
    
    for obj in decodedObjects:
        print("Type:", obj.type)
        print("Data: ", obj.data, "\n")
        
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break