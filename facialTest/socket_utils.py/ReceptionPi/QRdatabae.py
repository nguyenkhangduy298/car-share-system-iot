import sqlite3

DB_NAME = "QR.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

with conn:
    # connection.execute("""
    #             drop table Users
    #             """)

    # connection.execute("""
    #     create table Users (UserName text not null primary key,Password text not null, FirstName text not null, LastName text not null)
    #     """)
    conn.execute("""
        create table engineer (AccountID text not null, UserName text not null primary key, position text not null, phone text not null, email text not null)
        """)
    conn.execute("""
        insert into engineer (AccountID , UserName, position, phone, email) values ("N1311",'nhan','Engineer', '0908068013', 'pnthanhnhan1311@gmail.com')
        """)
    # connection.execute("""
    #     insert into Users (UserName, FirstName, LastName) values ('shekhar', 'Shekhar', 'Kalra')
    #     """)

conn.close()
