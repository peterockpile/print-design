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

from pdesign.widgets import ActionButton, UnitLabel

class ActionPlugin(gtk.HBox):

	def __init__(self, mw):
		gtk.HBox.__init__(self)
		self.mw = mw
		self.app = mw.app
		self.actions = self.app.actions
		self.sep = gtk.VSeparator()
		self.pack_end(self.sep, False, False, 5)
		self.build()

	def build(self):pass

class GroupPlugin(ActionPlugin):

	name = 'GroupPlugin'

	def build(self):
		self.rot_left = ActionButton(self.actions['GROUP'])
		self.pack_start(self.rot_left, False, False, 0)

		self.rot_left = ActionButton(self.actions['UNGROUP'])
		self.pack_start(self.rot_left, False, False, 0)

		self.rot_left = ActionButton(self.actions['UNGROUP_ALL'])
		self.pack_start(self.rot_left, False, False, 0)


class TestPlugin(ActionPlugin):

	name = 'TestPlugin'

	def build(self):
		self.pack_start(gtk.Label(self.name))

class Test1Plugin(ActionPlugin):

	name = 'Test1Plugin'

	def build(self):
		self.pack_start(gtk.Label(self.name))
