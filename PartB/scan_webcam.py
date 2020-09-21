import cv2
from database_utils import DatabaseUtils
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
    self.runQR()
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
        with DatabaseUtils() as db:
            for car in db.viewHistory(customerId):
                print( "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(customer[0], customer[1], 
                                                                    customer[2], customer[3], customer[4], 
                                                                    customer[5], customer[6], customer[7], 
                                                                    customer[8]))
cap.release()
cv2.destroyAllWindows()