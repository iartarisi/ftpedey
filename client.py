#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of ftpedey.
# Copyright (c) 2010 Ionuț Arțăriși

# ftpedey is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# ftpedey is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with ftpedey.  If not, see <http://www.gnu.org/licenses/>.

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
