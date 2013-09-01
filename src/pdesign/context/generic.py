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

import wx

from pdesign.widgets import ALL, EXPAND, LEFT, CENTER
from pdesign.widgets import HPanel, VLine, Label

class CtxPlugin(HPanel):

	app = None
	insp = None
	proxy = None
	actions = None

	name = 'Plugin'

	def __init__(self, app, parent):
		self.app = app
		self.insp = self.app.insp
		self.actions = self.app.actions
		HPanel.__init__(self, parent)
		self.build()
		self.add(VLine(self), 0, ALL | EXPAND, 2)
		self.hide()

class PL1(CtxPlugin):

	name = 'Plugin_1'

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)

	def build(self):
		self.add(Label(self, self.name), 0, LEFT | CENTER)

class PL2(CtxPlugin):

	name = 'Plugin_2'

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)

	def build(self):
		self.add(Label(self, self.name), 0, LEFT | CENTER)

class PL3(CtxPlugin):

	name = 'Plugin_3'

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)

	def build(self):
		self.add(Label(self, self.name), 0, LEFT | CENTER)




