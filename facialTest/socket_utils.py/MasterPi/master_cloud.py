#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sys
sys.path.append("..")
import socket_utils
from database_utils import DatabaseUtils

HOST = "0.0.0.0"    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 63000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

def main():
    with DatabaseUtils() as db:
        db.createCustomerTable()
        db.createCarTable()
        db.createBookHistoryTable()
        print(db.getCustomer())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()

        print("Listening on {}...".format(ADDRESS))
        while True:
            print("Waiting for Reception Pi...")
            conn, addr = s.accept()
            with conn:
                print("Connected to {}".format(addr))
                print()

                user = socket_utils.recvJson(conn)
                menu(user)

                socket_utils.sendJson(conn, { "logout": True })

def menu(user):
    while(True):
        print("Welcome {}".format(user["username"]))
        username = str(user["username"])
        password = str(user["password"])
        with DatabaseUtils() as db:
            for cust in db.getOneCust(property,username,password):
                if cust[0]=="":
                    message = "Warning!!! User Not Identified"
                else:
                    message = "Autheticated!!! User Identified"
                print(message)

# Execute program.
if __name__ == "__main__":
    main()
