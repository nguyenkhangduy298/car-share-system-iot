import sqlite3

DB_NAME = "reception.db"

connection = sqlite3.connect(DB_NAME)

with connection:
    connection.execute("""
                drop table Users
                """)

    connection.execute("""
        create table Users (UserName text not null primary key,Password text not null, FirstName text not null, LastName text not null)
        """)

    connection.execute("""
        insert into Users (UserName,Password, FirstName, LastName) values ('nhan','nhan', 'Matthew', 'Bolger')
        """)
    # connection.execute("""
    #     insert into Users (UserName, FirstName, LastName) values ('shekhar', 'Shekhar', 'Kalra')
    #     """)

connection.close()
