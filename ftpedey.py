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

        builder.get_object("PWD").connect("clicked", self.pwd)
        outputBox = builder.get_object("textview1")

        self.buf = gtk.TextBuffer()
        outputBox.set_buffer(self.buf)


    def destroy(self, widget, data=None):
        gtk.main_quit()

    def pwd(self, button):
        self.buf.insert_at_cursor(self.client.send("PWD"))
        

if __name__ == "__main__":
    hwg = HellowWorldGTK()
    gtk.main()
