import MySQLdb
# import pymysql
# from flask_login import UserMixin

class DatabaseUtils:

    HOST = "34.126.127.197"
    USER = "root"
    PASSWORD = "duy298"
    DATABASE = "carshare_iot_system"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    # -----------------------------------------------------------
    def createCustomerTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Customer (
                    CustomerID int not null auto_increment,
                    username text not null,
                    password text not null,
                    Name text not null, address text, phone text, fax text, email text, contact text,
                    constraint PK_Customer primary key (CustomerID)
                )""")
        self.connection.commit()

    def createCarTable(self):
        with self.connection.cursor() as cursor:

            cursor.execute("""
                create table if not exists Car (
                    CarID int not null auto_increment,status text,
                    Name text not null, model text, brand text, company text, colour text, seats int, description text, category text, cost_per_hour double not null, location text, CustomerID int,
                    constraint PK_Car primary key (CarID)
                
                )""")
        self.connection.commit()
        # constraint FK_Car FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID))

    def createBookHistoryTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                   create table if not exists BookHistory (
                       HistoryId int not null auto_increment,
                       status text,
                       CarID int, CustomerID int,
                       bookTime DATE , endTime DATE,
                       constraint PK_History primary key (HistoryID)
                       )""")
        self.connection.commit()
        # constraint FK_Car FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID))

    def getCustomer(self):
        print("GET CUSTOMER")
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Customer")
            return cursor.fetchall()

    def getCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Car")
            return cursor.fetchall()

    def registerAccount(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from customer")
            return cursor.fetchall()

    def getOneCar(self,property,value):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Car where "+property+"=\""+value+"\"")
            # cursor.execute("select * from Car where CarID=2")
            return cursor.fetchall()

    def viewHistory(self,custId):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Car where CustomerID="+str(custId))
            return cursor.fetchall()

    def getOneCust(self,username,password):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Customer where username=\""+username+"\" & password=\""+password+"\"")
            # cursor.execute("select * from Car where CarID=2")
            return cursor.fetchall()