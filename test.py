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
