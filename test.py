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

import client
import unittest

class CommandsCheck(unittest.TestCase):
    client = client.Client()
    def testPwd(self):
        self.assertEqual(self.client.send("PWD"), "PWD: ")

    def testUnknownCommand(self):
        self.assertEqual(self.client.send("caca"),
                         "500 Syntax error, command unrecognized.")

    def testCdup(self):
        pass

    def testNoop(self):
        self.assertEqual(self.client.send("NOOP"), "OK")
    def testMkdandRmd(self):
        '''Create dir and try to create it again. Also delete it twice.
        '''
        # FIXME: testcases should be independent and modular
        # but at least this way we clean up after ourselves
        self.assertEqual(self.client.send("MKD dum"),
                         "S-a creat directorul 'dum'.")
        self.assertEqual(self.client.send("MKD dum"),
                         "Directorul exista deja.")
        self.assertEqual(self.client.send("RMD dum"),
                         "Directorul 'dum' a fost sters.")
        self.assertEqual(self.client.send("RMD dum"),
                         "Directorul 'dum' nu exista.")
    
    def testNodirMkd(self):
        self.assertEqual(self.client.send("MKD"),
                       "Comanda MKD primeste ca argument numele directorului.")
    def testNodirRmd(self):
        self.assertEqual(self.client.send("RMD"),
                       "Comanda RMD primeste ca argument numele directorului.")

    def testCwd(self):
        self.client.send("MKD dum")
        self.assertEqual(self.client.send("CWD dum"),
                         "CWD: /dum")
        self.client.send("CDUP")
        self.client.send("RMD dum")
        
if __name__ == "__main__":
    unittest.main()
