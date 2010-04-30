#!/usr/bin/python

import gtk
import gtk.glade
import gnome.ui
import pygtk
import client


class HellowWorldGTK:
    """This is an Hello World GTK application"""

    def __init__(self):

        #Set the Glade file
        builder = gtk.Builder()
        builder.add_from_file("ftpedey.glade")
        self.window = builder.get_object("window1")
        self.window.show()
        self.client = client.Client()

        # builder.get_object("PWD").connect("clicked", self.pwd)
        outputBox = builder.get_object("textview1")
        self.buf = gtk.TextBuffer()
        outputBox.set_buffer(self.buf)

        self.entry = builder.get_object("entry1")
        builder.connect_signals(self)

    def pwd(self, button):
        self.buf.insert_at_cursor(self.client.send("PWD"))

    def cdup(self, button):
        self.buf.insert_at_cursor(self.client.send("CDUP"))

    def cwd(self, button):
        data = self.entry.get_text()
        self.buf.insert_at_cursor(self.client.send("CWD %s" % data))

    def rmd(self, button):
        data = self.entry.get_text()
        self.buf.insert_at_cursor(self.client.send("RMD %s" % data))

    def mkd(self, button):
        data = self.entry.get_text()
        self.buf.insert_at_cursor(self.client.send("MKD %s" % data))
                                  
    def destroy(self, widget, data=None):
        gtk.main_quit()
        

if __name__ == "__main__":
    hwg = HellowWorldGTK()
    gtk.main()
