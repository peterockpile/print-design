#! /usr/bin/python
#
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

from pdesign.widgets import const, BOTTOM, CENTER, LEFT, ALL, EXPAND
from pdesign.widgets import Application, MainWindow, Button
from pdesign.widgets import HPanel, VPanel

class TabButton(Button):

	def __init__(self, parent, txt=''):
		self.txt = txt
		Button.__init__(self, parent, txt, onclick=self.clicked)

	def clicked(self, *args):
		print 'clicked ' + self.txt


class TabPanel(HPanel):

	def __init__(self, parent):
		HPanel.__init__(self, parent)

		for item in range(5):
			self.add(TabButton(self, 'Tab_' + str(item),))
		self.SetSize(self.GetBestSize())

class TabNavPanel(HPanel):

	def __init__(self, parent):
		HPanel.__init__(self, parent)

		self.b_left = Button(self, '<', onclick=self.scroll_left)
		self.add(self.b_left)

		self.scrollwin = HPanel(self)
		self.scrollwin.SetBackgroundColour(wx.WHITE)
		self.add(self.scrollwin, 1, ALL | EXPAND)

		self.tab_panel = TabPanel(self.scrollwin)
		self.tab_panel.SetPosition((0, 0))

		self.b_right = Button(self, '>', onclick=self.scroll_right)
		self.add(self.b_right)

	def scroll_left(self, *args):
		x = self.tab_panel.GetPosition()[0]
		x -= 10
		self.tab_panel.SetPosition((0, 0))
		self.tab_panel.SetPosition((x, 0))
		print 'scroll_left', x

	def scroll_right(self, *args):
		x = self.tab_panel.GetPosition()[0]
		x += 10
		self.tab_panel.SetPosition((0, 0))
		self.tab_panel.SetPosition((x, 0))
		print 'scroll_right', x

class WidgetPanel(VPanel):

	nav_p = None

	def __init__(self, parent):
		VPanel.__init__(self, parent)
		self.build()

	def build(self):
		flags = LEFT | CENTER
		pflags = ALL | EXPAND

		p = HPanel(self)
		self.add(p, 0, pflags)
		p.add(Button(p, '+', onclick=self.add_tab))
		p.add(Button(p, '-', onclick=self.remove_tab))

		self.nav_p = TabNavPanel(self)
		self.add(self.nav_p, 0, pflags)


	def add_tab(self, *args):
		print 'add_tab'


	def remove_tab(self, *args):
		print 'remove_tab'


app = Application('wxWidgets')
mw = MainWindow('Scrolled Tabs', (600, 250))
p = VPanel(mw)
mw.add(p, 1, ALL | EXPAND)
panel = WidgetPanel(mw)
p.add(panel, 1, ALL | EXPAND, 10)
app.mw = mw
app.run()
