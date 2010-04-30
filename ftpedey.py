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
