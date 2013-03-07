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

from pdesign.widgets import ActionButton

class ActionPlugin(gtk.HBox):

	def __init__(self, mw):
		gtk.HBox.__init__(self)
		self.mw = mw
		self.app = mw.app
		self.actions = self.app.actions
		self.sep = gtk.VSeparator()
		self.pack_end(self.sep, False, False, 2)
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

class RotatePlugin(ActionPlugin):

	name = 'RotatePlugin'

	def build(self):
		self.rot_left = ActionButton(self.actions['ROTATE_LEFT'])
		self.pack_start(self.rot_left, False, False, 0)

		self.rot_right = ActionButton(self.actions['ROTATE_RIGHT'])
		self.pack_start(self.rot_right, False, False, 0)

class MirrorPlugin(ActionPlugin):

	name = 'MirrorPlugin'

	def build(self):
		self.rot_left = ActionButton(self.actions['HOR_MIRROR'])
		self.pack_start(self.rot_left, False, False, 0)

		self.rot_right = ActionButton(self.actions['VERT_MIRROR'])
		self.pack_start(self.rot_right, False, False, 0)

class CombinePlugin(ActionPlugin):

	name = 'CombinePlugin'

	def build(self):
		self.rot_left = ActionButton(self.actions['COMBINE'])
		self.pack_start(self.rot_left, False, False, 0)

		self.rot_right = ActionButton(self.actions['BREAK_APART'])
		self.pack_start(self.rot_right, False, False, 0)

class ToCurvePlugin(ActionPlugin):

	name = 'ToCurvePlugin'

	def build(self):
		self.but = ActionButton(self.actions['CONVERT_TO_CURVES'])
		self.pack_start(self.but, False, False, 0)



