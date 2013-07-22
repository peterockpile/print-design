# -*- coding: utf-8 -*-
#
#	Copyright (C) 2012 by Igor E. Novikov
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


from pdesign import _, events, icons
from pdesign.plugins.plg_caption import PluginTabCaption

class PagesPlugin(gtk.VBox):

	name = 'PagesPlugin'
	title = _('Pages roll')
	icon = icons.STOCK_PLUGIN_PAGES
	loaded = False
	active = False

	def __init__(self, master):
		gtk.VBox.__init__(self)
		self.master = master
		self.mw = master.mw
		self.app = master.app
		self.caption = PluginTabCaption(self, self.icon, self.title)

	def build(self):
		self.label = gtk.Label()
		self.label.set_text(str(self.active))
		self.pack_start(self.label)
		self.loaded = True

	def activate(self):
		self.active = True
		self.label.set_text(str(self.active))

	def deactivate(self):
		self.active = False
		self.label.set_text(str(self.active))
