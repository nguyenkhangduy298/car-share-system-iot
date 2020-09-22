import bluetooth
import cv2
import face_recognition
import numpy as np
import time
import socket, json, sqlite3, sys
sys.path.append("..")
import socket_utils
DB_NAME ="reception.db"



cap = cv2.VideoCapture(-1)
detector = cv2.QRCodeDetector()

with open("config.json","r") as file:
    data = json.load(file)

HOST = data["masterpi_ip"]   # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

def runMenu():
    while(True):
        print()
        print("1. engineer")
        print("2. user")
        selection = input("Select an option: ")
        print()
        if(selection == "1"):
            print()
            print("3. scan QR")
            print("4. open the car")
            selection1 = input("Select an option: ")
            print()
            if (selection1 == "3"):
                while True:
                    _, img = cap.read()
                    data, bbox, _ = detector.detectAndDecode(img)
                            
                    if(bbox is not None):
                        for i in range(len(bbox)):
                            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                                            0, 255), thickness=2)
                            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5, (0, 255, 0), 2)
                            # conn = sqlite3.connect(DB_NAME)
                            # conn.row_factory = sqlite3.Row
                            row1 = getEngineer(data)
                            loginEng(row1)
                            # with conn:
                            #     c = conn.cursor()
                            #     c.execute("SELECT * FROM engineerTest WHERE AccountID = ?", (data))
                            #     row = c.fetchone()
                            #     print(row)
                    cv2.imshow("code detector", img)
                    if(cv2.waitKey(1) == ord("q")):
                        break
            else:
                print("Performing inquiry...")

                nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                                                flush_cache=True, lookup_class=False)

                print("Found {} devices".format(len(nearby_devices)))

                for addr, name in nearby_devices:
                    try:
                        print("   {} - {}".format(addr, name))
                        if addr == "8C:83:E1:D0:84:03":
                            print ("the car is open")
                        else:
                            print ("Alert")
                    except UnicodeEncodeError:
                        print("   {} - {}".format(addr, name.encode("utf-8", "replace")))
        else:
            print()
            print("1. use the username and password")
            print("2. facial checking")
            selection2 = input("Select an option: ")
            print()
            if (selection2 == "1"):
                name = input("username: ")
                password = input("password:")
                user = getUser(name,password)
                login(user)
            else:
                # Load a sample picture and learn how to recognize it.
                picture_of_me = face_recognition.load_image_file("nhan.jpg")
                my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

                # Load a second sample picture and learn how to recognize it.
                duy = face_recognition.load_image_file("duy.jpg")
                duy_face_encoding = face_recognition.face_encodings(duy)[0]

                # Create arrays of known face encodings and their names
                known_face_encodings = [
                    my_face_encoding,
                    duy_face_encoding
                ]
                known_face_names = [
                    "Thanh Nhan","Khang Duy"
                    
                ]

                # Initialize some variables
                face_locations = []
                face_encodings = []
                face_names = []
                process_this_frame = True
                count=0
                # dbx = dropbox.Dropbox('6lYXOy3Wb2AAAAAAAAAADjd3j3ycNSoJ7e3FoakEJ-hqk3DMeMsPZe-9TVZAFilf')
                # Get a reference to webcam #0 (the default one)
                while True:
                    var = input("Launch The Security Service? ")
                    if str(var) == "Yes":
                        break

                while True:
                    # Grab a single frame of video
                    ret, frame = cap.read()
                    # Resize frame of video to 1/4 size for faster face recognition processing
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                    rgb_small_frame = small_frame[:, :, ::-1]

                    # Only process every other frame of video to save time
                    if process_this_frame:
                        # Find all the faces and face encodings in the current frame of video
                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                        face_names = []
                        for face_encoding in face_encodings:
                            # See if the face is a match for the known face(s)
                            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                            name = "Unknown"
                            # If a match was found in known_face_encodings, just use the first one.
                            if True in matches:
                                first_match_index = matches.index(True)
                                name = known_face_names[first_match_index]

                            face_names.append(name)
                            if name == "Unknown":
                                print("Unknown people Warning")
                            else:
                                print("Car Door Opening...!!!!")
                                break
                    process_this_frame = not process_this_frame

                    # Display the results
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4
                    
                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    
                        # Draw a label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    
                    # Display the resulting image
                    cv2.imshow('Video', frame)

                    # Hit 'q' on the keyboard to quit!
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("System Shutdown!!")
                        break

def getUser(username,password):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    with connection:
        cursor = connection.cursor()
        cursor.execute("select * from Users where UserName = ? and Password = ?", (username,password))
        row = cursor.fetchone()
    connection.close()

    return { "username": row["UserName"], "firstname": row["FirstName"], "lastname": row["LastName"]  }

def getEngineer(AccountID):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    with connection:
        cursor = connection.cursor()
        cursor.execute("select Name, phone, email from Engineers where AccountID = ? ", (AccountID))
        row = cursor.fetchone()
    connection.close()

    return { "name": row["Name"], "phone": row["phone"], "email": row["email"]  }


def login(user):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        print("Logging in as {}".format(user["username"]))
        socket_utils.sendJson(s, user)

        print("Waiting for Master Pi...")
        while(True):
            object = socket_utils.recvJson(s)
            if("logout" in object):
                print("Master Pi logged out.")
                print()
                break

def loginEng(engineer):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        print("Logging in as {}".format(engineer["username"]))
        socket_utils.sendJson(s, engineer)

        print("Waiting for Master Pi...")
        while(True):
            object = socket_utils.recvJson(s)
            if("logout" in object):
                print("Master Pi logged out.")
                print()
                break

if __name__ == "__main__":
    runMenu()