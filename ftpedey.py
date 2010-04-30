#!/usr/bin/python

import gtk
import gtk.glade
import gnome.ui
import pygtk
import client


class FtpedeyGTK:
    def __init__(self):
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

    def show(self, text):
        self.buf.insert_at_cursor(text + '\n')

    def pwd(self, button):
        self.show(self.client.send("PWD"))

    def cdup(self, button):
        self.show(self.client.send("CDUP"))

    def cwd(self, button):
        data = self.entry.get_text()
        self.show(self.client.send("CWD %s" % data))

    def rmd(self, button):
        data = self.entry.get_text()
        self.show(self.client.send("RMD %s" % data))

    def mkd(self, button):
        data = self.entry.get_text()
        self.show(self.client.send("MKD %s" % data))

    def retr(self, button):
        remote_name = self.entry.get_text()
        fc = gtk.FileChooserDialog(title="Alege unde se va salva fisierul",
                                   action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                   buttons=(gtk.STOCK_CANCEL,
                                            gtk.RESPONSE_CANCEL,
                                            gtk.STOCK_SAVE,
                                            gtk.RESPONSE_OK))
        if fc.run() == gtk.RESPONSE_OK:
		local_name = fc.get_filename()
	fc.destroy()

        f = open(local_name, "w")
        f.write(self.client.retr(remote_name))
        f.close()
        self.show("RETR %s" % remote_name)
        
    def destroy(self, widget, data=None):
        gtk.main_quit()
        

if __name__ == "__main__":
    hwg = FtpedeyGTK()
    gtk.main()
