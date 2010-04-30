#!/usr/bin/env python

import socket
import sys

HOST, PORT = "localhost", 5000

class Client:
    def send(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
        sock.close()
        return received
    
    def retr(self, fname):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        sock.connect((HOST, PORT))
        sock.send("RETR %s\n" % fname)
        received =""
        while True:
            lastbit = sock.recv(1024)
            if not lastbit:
                break
            received += lastbit
        sock.close()
        return received
        
if __name__ == "__main__":
    client = Client()
    data = " ".join(sys.argv[1:])
    print "In:  %s" % data
    print "Out: %s" % client.send(data)
