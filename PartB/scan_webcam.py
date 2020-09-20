import cv2
from main import Customer
from flask_sqlalchemy import SQLAlchemy

cap = cv2.VideoCapture(1)

detector = cv2.QRCodeDetector()

def main(self):
    with Customer() as db:
        db.createCustomerTable()
        db.createCarTable()
        db.createBookHistoryTable()
        db.createExecutiveTable()
        print(db.getCustomer())

def runQR(self):
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

def viewHistory(self,CustomerID):
        print("-----View profile------------")
        print( "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t <br>".format(customer.CustomerID,
                                                            customer.username,
                                                            customer.Name,
                                                            customer.address,
                                                            customer.phone,
                                                            customer.fax,
                                                            customer.email,
                                                            customer.contact))
cap.release()
cv2.destroyAllWindows()