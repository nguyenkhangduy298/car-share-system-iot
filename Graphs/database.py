import MySQLdb
from datetime import date

class Database:
    def __init__(self, host, username, password, database):
        self.connection = MySQLdb.connect(host, username, password, database)
        self.cursor = self.connection.cursor()

    def createActiveUserTable(self):
        self.cursor.execute("""
            create table if not exists ActiveUser (
                date date not null,
                total_active_user int not null
            )""")
        self.connection.commit()
        

    def insertActiveUser(self, current_date, total_active_user):
        request = ("INSERT INTO ActiveUser (date, total_active_user) VALUES ( %s, %s)")
        add_data = (current_date, total_active_user)
        self.cursor.execute(request, add_data)
        self.connection.commit()

    def updateActiveUser(self, current_date, total_active_user):
        request = 'UPDATE ActiveUser SET total_active_user=%s WHERE date=%s'
        add_data = (total_active_user, current_date)
        self.cursor.execute(request, add_data)
        self.connection.commit()

    def getAllActiveUser(self):
        self.cursor.execute("select * from ActiveUser")
        return self.cursor.fetchall()

    def countRows(self):
        return self.cursor.rowcount

# -----------------------------------------------------------------------------
    def getAllBookHistory(self):
        self.cursor.execute("select CarID, bookTime from BookHistory")
        return self.cursor.fetchall()
    
    def getCarByID(self, carID):
        request = "select Name from Car where CarID=%s"
        add_data = carID
        self.cursor.execute(request, add_data)
        return self.cursor.fetchall()

    def getCars(self):
        self.cursor.execute("select CarID, Name from Car")
        return self.cursor.fetchall()



