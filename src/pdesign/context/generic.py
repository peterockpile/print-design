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

from pdesign.widgets import ALL, EXPAND
from pdesign.widgets import HPanel, VLine

class CtxPlugin(HPanel):

	app = None
	insp = None
	proxy = None
	actions = None

	name = 'Plugin'

	def __init__(self, app, parent):
		self.app = app
		self.parent = parent
		self.insp = self.app.insp
		self.actions = self.app.actions
		HPanel.__init__(self, parent)
		self.build()
		self.add(VLine(self), 0, ALL | EXPAND, 2)
		self.hide()





