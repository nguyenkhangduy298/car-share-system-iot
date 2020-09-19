from database import Database
from plot import Plot
import datetime

class Graphs:

    @staticmethod
    def get_xy(x, y, rows):
        for row in rows:
            x.append(row[0])
            y.append(row[1])

        for i in range(0, len(x)):
            x[i] = x[i].strftime ('%d-%m-%Y')

    # ------------------------------Plot daily active user-----------------------------------------
    @staticmethod
    def plot_daily_active_user():
        db = Database('35.201.22.166', "root", "123456", "ActiveUser")
        # db.createActiveUserTable()
        no_of_rows = db.countRows()
        x = []
        y = []
        if no_of_rows <= 7:
            rows = db.getAllActiveUser()
            Graphs.get_xy(x, y, rows)
        else:
            rows = db.getAllActiveUser()[-7:]
            Graphs.get_xy(x, y, rows)

        Plot.plot_line_chart(x, y, "Number of daily active user")

    # ----------------------------Plot number of booking by cars in current month----------------------------------
    @staticmethod
    def plot_bookings_by_cars():
        curr_month = datetime.date.today().month
        x = []
        y = []

        db = Database('34.126.127.197', "root", "duy298", "carshare_iot_system")

        for row in db.getCars():
            if row[1] not in x:
                x.append(row[1])
                y.append(0)

        for row in db.getAllBookHistory():
            for i in range(0, len(x)):
                if x[i] == db.getCarByID(str(row[0]))[0][0] and curr_month == row[1].month:
                    y[i] = y[i] + 1
        Plot.plot_bar_chart(x, y, "Number of bookings by cars")

    # ----------------------------Plot number of bookings monthly-------------------------------------
    @staticmethod
    def plot_monthly_booking():
        x = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", 
        "November", "December"]
        y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        db = Database('34.126.127.197', "root", "duy298", "carshare_iot_system")
        for row in db.getAllBookHistory():
            for i in range(len(x)):
                if row[1].month == i + 1:
                    y[i] = y[i] + 1

        Plot.plot_pie_chart(x, y, "Number of bookings monthly")

# When manager log in successfully, then:
Graphs.plot_daily_active_user()
Graphs.plot_bookings_by_cars()
Graphs.plot_monthly_booking()

# -----------------If customer login successfully, then: (to update ActiveUser table)
    # db = Database('35.201.22.166', "root", "123456", "ActiveUser")
    # db.createActiveUserTable()
    # today = datetime.date.today()
    # all_rows = db.getAllActiveUser()
    # if db.countActiveUser() != 0 and today == all_rows[-1][0]:
    #     new_num = all_rows[-1][1] + 1
    #     db.updateActiveUser(today, new_num)
    # else:
    #     db.insertActiveUser(today, 1)

    # for row in db.getAllActiveUser():
    #     print(row[0], row[1])

    
