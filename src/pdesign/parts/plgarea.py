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
from pdesign.widgets import HPanel, VPanel, ALL, EXPAND, VLine

class PlgArea(HPanel):

	app = None
	active_plg = None
	plugins = []
	container = None
	tabs = None

	def __init__(self, app, parent):
		self.app = app
		HPanel.__init__(self, parent)
		line = VLine(self)
		self.add(line, 0, ALL | EXPAND)
		self.container = VPanel(self)
		self.add(self.container, 1, ALL | EXPAND)
		self.tabs = PlgTabsPanel(app, self)
		self.add(self.tabs, 0, ALL | EXPAND)
		self.Layout()

	def check_id(self, pid):
		for item in self.plugins:
			if item.id == pid:
				return item
		return None

	def load_plugin(self, pid):
		item = self.app.plugins[pid]
		item.activate()
		self.plugins.append(item)
		return item

	def show_plugin(self, pid):
		if self.active_plg and pid == self.active_plg.pid: return
		item = self.check_id(pid)
		if self.active_plg:
			self.active_plg.hide()
		if not item:
			item = self.load_plugin(pid)
			self.container.add(item.panel, 1, ALL | EXPAND)
		self.active_plg = item
		self.active_plg.show()
		self.container.Layout()
		self.Layout()

class PlgTabsPanel(VPanel):

	app = None
	active_plg = None
	plugins = []
	container = None
	tabs = None

	def __init__(self, app, parent):
		self.app = app
		VPanel.__init__(self, parent)
		self.SetBackgroundColour(wx.Colour(183, 183, 183))
		self.add((10, 10))
