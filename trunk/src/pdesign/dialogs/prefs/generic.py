# -*- coding: utf-8 -*-
#
#	Copyright (C) 2013 by Igor E. Novikov
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

from pdesign import appconst

class GenericPrefsPlugin(gtk.VBox):

	app = None
	name = ''
	title = ''
	short_title = ''
	icon = gtk.STOCK_PROPERTIES
	cid = appconst.PREFS_APP_PLUGIN
	childs = []
	built = False
	leaf = True

	def __init__(self, app):
		gtk.VBox.__init__(self)
		self.app = app

	def build(self):
		title = gtk.Label()
		title.set_markup('<span size="large"><b>%s</b></span>' % (self.title))
		self.pack_start(title, False, False, 0)
		self.pack_start(gtk.HSeparator(), False, False, 5)
		self.built = True

	def apply_changes(self):pass