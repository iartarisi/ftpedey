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

import os
import SocketServer

class MyTCPHandler(SocketServer.StreamRequestHandler):
    os.chdir("data")
    rootdir = os.getcwd()
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "%s wrote: %s" % (self.client_address[0], self.data)
        self.data = self.data.split()

        if self.data[0] == "PWD":
            self.retrel(self.pwd())
        elif self.data[0] == "CDUP":
            self.retrel(self.cdup())
        elif self.data[0] == "MKD":
            self.retrel(self.mkd())
        elif self.data[0] == "RMD":
            self.retrel(self.rmd())
        elif self.data[0] == "CWD":
            self.retrel(self.cwd())
        elif self.data[0] == "NOOP":
            self.retrel(self.noop())
        elif self.data[0] == "RETR":
            self.wfile.write(self.retr())
        else:
            self.wfile.write("500 Syntax error, command unrecognized.")

    def retrel(self, directory):
        '''Returns a relative path to the root of the ftp
        '''
        return self.wfile.write(directory.replace(self.rootdir, "", 1))

    def pwd(self):
        return "PWD: %s" % os.getcwd()

    def cdup(self):
        if len(self.data) == 1:
            os.chdir('../')
            return "CDUP: %s" % os.getcwd()
        else:
            return "Comanda CDUP nu accepta parametri."

    def mkd(self):
        try:
            os.mkdir(self.data[1])
            return "S-a creat directorul '%s'." % self.data[1]
        except OSError:
            return "Directorul exista deja."
        except IndexError:
            return "Comanda MKD primeste ca argument numele directorului."

    def rmd(self):
        try:
            os.rmdir(self.data[1])
            return "Directorul '%s' a fost sters." % self.data[1]
        except OSError as (errno, strerror):
            if errno == 2:
                return "Directorul '%s' nu exista." % self.data[1]
        except IndexError:
            return "Comanda RMD primeste ca argument numele directorului."
    def cwd(self):
        try:
            os.chdir(self.data[1])
        except IndexError:
            return "Comanda CWD primeste ca argument numele directorului."
        except OSError as (errno, strerror):
            if errno == 2:
                return "Directorul '%s' nu exista." % self.data[1]
        else:
            return "CWD: %s" % os.getcwd()
    def noop(self):
        return "OK"
    def retr(self):
        try:
            f = open(self.data[1], 'rb')
        except IOError as (errno, strerror):
            if errno == 2:
                return self.wfile.write("Fisierul '%s' nu exista.")
        else:
            fcontent = f.read()
            f.close()
            return self.wfile.write(fcontent)


if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
