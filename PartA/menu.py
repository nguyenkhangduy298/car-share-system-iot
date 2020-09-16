from database_utils import DatabaseUtils

class Menu:
    def main(self):
        with DatabaseUtils() as db:
            db.createCustomerTable()
            db.createCarTable()
            db.createBookHistoryTable()
            print(db.getCustomer())

        self.runMenu()

    def runMenu(self):
        while(True):
            print()
            print("0. View Car History")
            print("1. Search A Car")
            print("2. Book A Car")
            print("3. Cancel A Booking")
            print("4. Log Out")
            selection = input("Select an option: ")
            print()

            if(selection == "0"):
                custId = 1
                self.viewHistory(custId)
            elif (selection == "1"):
                property = str(input("Choose Car Properties: "))
                value = str(input("Define Properties: "))
                print(property,value)
                self.searchCar(property,value)
            elif(selection == "2"):
                id = str(input("Choose CarID to book: "))
                duration = input("Input Booking Duration (days): ")
                property="CarID"
                self.searchCar(property,id)
            elif (selection == "3"):
                self.insertPerson()
            elif(selection == "4"):
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def viewHistory(self,custId):
        print("-----View Car History------------")
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format("CarID","Status", "Name", "Model", "Brand","Company", "Colour", "Seats", "Description","Category", "CostPerHour","Location","CustID"))
        with DatabaseUtils() as db:
            for car in db.viewHistory(custId):
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], car[10], car[11], car[12]))

    def searchCar(self,property,value):
        print("-----Car Searched-------------")
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format("CarID","Status", "Name", "Model", "Brand","Company", "Colour", "Seats", "Description","Category", "CostPerHour","Location","CustID"))
        with DatabaseUtils() as db:
            for car in db.getOneCar(property,value):
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], car[10], car[11], car[12]))

    def insertPerson(self):
        print("--- Insert Person ---")
        name = input("Enter the person's name: ")
        with DatabaseUtils() as db:
            if(db.insertPerson(name)):
                print("{} inserted successfully.".format(name))
            else:
                print("{} failed to be inserted.".format(name))

if __name__ == "__main__":
    Menu().main()
