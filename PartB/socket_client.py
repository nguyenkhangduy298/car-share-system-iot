#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, pprint, socket_utils
import cv2
cap = cv2.VideoCapture(-1)
detector = cv2.QRCodeDetector()
_, img = cap.read()
data, bbox, _ = detector.detectAndDecode(img)

HOST = input("Enter IP address of server: ")

# HOST = "127.0.0.1" # The server's hostname or IP address.
PORT = 64000       # The port used by the server.
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to {}...".format(ADDRESS))
    s.connect(ADDRESS)
    print("Connected.")

    while True:
        message = input(data)
        if(not message):
            socket_utils.sendJson(s, { "end": True })
            break

        socket_utils.sendJson(s, { "message": message })
        object = socket_utils.recvJson(s)

        print("Received:")
        pprint.pprint(object)
        print(object["message"])

    print("Disconnecting from server.")
print("Done.")
