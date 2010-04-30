#!/usr/bin/env python -c

import socket
import sys

HOST, PORT = "localhost", 5000

class Client:
    def send(self, data):
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.send(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
        sock.close()
        return received

if __name__ == "__main__":
    client = Client()
    data = " ".join(sys.argv[1:])
    print "In:  %s" % data
    print "Out: %s" % client.send(data)
