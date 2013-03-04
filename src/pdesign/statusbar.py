# -*- coding: utf-8 -*-
#
#	Copyright (C) 2011-2012 by Igor E. Novikov
#	
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#	
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>. 


import gtk

from pdesign import events
from pdesign.widgets.color_monitor import ColorMonitorWidget

class AppStatusbar(gtk.Statusbar):

	def __init__(self, mw):
		gtk.Statusbar.__init__(self)

		self.mw = mw
		self.app = mw.app
		self.build()
		events.connect(events.APP_STATUS, self.show_message)

	def build(self):
		self.cmw = ColorMonitorWidget(self.app)
		self.pack_end(self.cmw, False, False, 0)

		vbox = gtk.VBox()
		spacer = gtk.EventBox()
		vbox.pack_start(spacer, False, False, 10)
		self.pack_end(vbox, False, False, 0)

	def show_message(self, args):
		self.push(0, args[0])
