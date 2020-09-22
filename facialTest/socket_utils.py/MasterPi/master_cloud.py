#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sys
sys.path.append("..")
import socket_utils
from database_utils import DatabaseUtils

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
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
        username = "".format(user["username"])
        password = "".format(user["password"])
        with DatabaseUtils() as db:
            for car in db.getOneCust(property,username,password):
                print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], car[10], car[11], car[12]))


# Execute program.
if __name__ == "__main__":
    main()
