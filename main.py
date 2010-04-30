#!/usr/bin/env python
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
        else:
            self.wfile.write("500 Syntax error, command unrecognized.")

    def retrel(self, directory):
        '''Returns a relative path to the root of the ftp
        '''
        return self.wfile.write(directory.replace(self.rootdir, "", 1) + "\n")

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
        else:
            return "CWD: %s" % os.getcwd()
    def noop(self):
        return "OK"

if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
