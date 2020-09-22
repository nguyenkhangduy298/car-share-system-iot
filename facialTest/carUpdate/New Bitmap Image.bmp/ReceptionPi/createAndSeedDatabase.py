import sqlite3

DB_NAME = "reception.db"

connection = sqlite3.connect(DB_NAME)

with connection:
    # connection.execute("""
    #             drop table Users
    #             """)
    # connection.execute("""
    #             drop table Engineers
    #             """)

    connection.executescript("""
        create table Users (UserName text not null primary key,Password text not null, FirstName text not null, LastName text not null);
        create table Engineers (AccountID text not null  primary key, Name text not null, position text not null, phone text not null, email text not null)
        """)
    # connection.execute("""
    #     create table Engineers (AccountID text not null  primary key, Name text not null, position text not null, phone text not null, email text not null)
    #     """)
    # connection.execute("""
    #     create table engineerTest (AccountID text not null  primary key, Name text not null, position text not null, phone text not null, email text not null)
    #     """)
    # connection.execute("""
    #     insert into engineerTest (AccountID , Name, position, phone, email) values ('N1311','nhan','Engineer', '0908068013', 'pnthanhnhan1311@gmail.com')
    #     """)
    connection.execute("""
        insert into Engineers (AccountID , Name, position, phone, email) values ('N1311','nhan','Engineer', '0908068013', 'pnthanhnhan1311@gmail.com')
        """)
    # connection.execute("""
    #     insert into Users (UserName, FirstName, LastName) values ('shekhar', 'Shekhar', 'Kalra')
    #     """)

connection.close()
