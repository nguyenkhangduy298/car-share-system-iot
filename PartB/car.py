import bluetooth

cap = cv2.VideoCapture(-1)
detector = cv2.QRCodeDetector()

def runMenu(self):
        while(True):
            print()
            print("1. engineer")
            print("2. user")
            selection = input("Select an option: ")
            print()
            if(selection == "1"):
                print()
                print("1. scan QR")
                print("2. open the car")
                selection1 = input("Select an option: ")
                print()
                if (selection1 == 1):
                    while True:
                        _, img = cap.read()
                        data, bbox, _ = detector.detectAndDecode(img)
                            
                        if(bbox is not None):
                            for i in range(len(bbox)):
                                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                                            0, 255), thickness=2)
                                cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5, (0, 255, 0), 2)
                                if (data == CustomerID) and (session["position"] == "engineer") :
                                    self.viewHistory(CustomerID)
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
                if (selection2 == 1):
                    username = input("username: ")
                    password = input("password:")
                else:

