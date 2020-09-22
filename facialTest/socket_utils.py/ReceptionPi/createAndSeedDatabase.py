import sqlite3

DB_NAME = "reception.db"

connection = sqlite3.connect(DB_NAME)

with connection:
    connection.execute("""
                drop table Users
                """)
    connection.execute("""
                drop table engineer
                """)

    connection.execute("""
        create table Users (UserName text not null primary key,Password text not null, FirstName text not null, LastName text not null)
        """)
    connection.execute("""
        create table engineer (AccountID text not null  primary key, UserName text not null, position text not null, phone text not null, email text not null)
        """)
    connection.execute("""
        insert into engineer (AccountID , UserName, position, phone, email) values ("N1311",'nhan','Engineer', '0908068013', 'pnthanhnhan1311@gmail.com')
        """)
    # connection.execute("""
    #     insert into Users (UserName, FirstName, LastName) values ('shekhar', 'Shekhar', 'Kalra')
    #     """)

connection.close()
