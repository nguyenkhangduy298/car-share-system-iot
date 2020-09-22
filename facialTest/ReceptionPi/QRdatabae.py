import sqlite3

DB_NAME = "engineer.db"

conn = sqlite3.connect(DB_NAME)

with conn:
    # connection.execute("""
    #             drop table Users
    #             """)
    conn.execute("""
                drop table Engineers
                """)
    # connection.execute("""
    #     create table Users (UserName text not null primary key,Password text not null, FirstName text not null, LastName text not null)
    #     """)
    conn.execute("""
        create table Engineers (AccountID text not null  primary key, Name text not null, position text not null, phone text not null, email text not null)
        """)
    sqlite_insert_query = """INSERT INTO  Engineers (AccountID , Name, position, phone, email)  VALUES  ('N1311', 'nhan', 'Engineer', '0908068013', 'pnthanhnhan1311@gmail.com')"""
    # conn.execute("""
    #     insert into Engineers (AccountID , Name, position, phone, email) values ('N1311','nhan','Engineer', '0908068013', 'pnthanhnhan1311@gmail.com')
    #     """)
    # connection.execute("""
    #     insert into Users (UserName, FirstName, LastName) values ('shekhar', 'Shekhar', 'Kalra')
    #     """)
cursor = conn.cursor()
print("Successfully Connected to SQLite")
count = cursor.execute(sqlite_insert_query)
conn.commit()
print("SQLite table created")
print("Record inserted successfully into Engineers table ", cursor.rowcount)
conn.close()
