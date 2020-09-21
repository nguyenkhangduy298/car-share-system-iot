import bluetooth
import cv2
import socket, json, sys
sys.path.append("..")
import socket_utils

cap = cv2.VideoCapture(-1)
detector = cv2.QRCodeDetector()

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
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
                            if(data == "nhan"):
                                print("profile!!!")
                                # if (data == CustomerID) and (session["position"] == "engineer") :
                                    # self.viewHistory(CustomerID)
                                break
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
                print("scan your face")

def getUser(username,password):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    with connection:
        cursor = connection.cursor()
        cursor.execute("select * from Users where UserName = ? and Password = ?", (username,password,))
        row = cursor.fetchone()
    connection.close()

    return { "username": row["UserName"], "firstname": row["FirstName"], "lastname": row["LastName"]  }

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

if __name__ == "__main__":
    runMenu()