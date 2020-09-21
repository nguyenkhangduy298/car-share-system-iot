#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, pprint, socket_utils

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 64000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    print("Listening on {}...".format(ADDRESS))
    conn, addr = s.accept()
    with conn:
        print("Connected to {}".format(addr))

        while True:
            object = socket_utils.recvJson(conn)
            if("end" in object):
                break

            print("Received:")
            pprint.pprint(object)
            print(object["message"])

            print("Sending data back.")
            socket_utils.sendJson(conn, object)

        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")
