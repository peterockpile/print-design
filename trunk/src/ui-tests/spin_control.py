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
from pdesign.widgets import Application, MainWindow, Entry
from pdesign.widgets import HPanel, VPanel
from pdesign.widgets.basic import SpinButton, SizedPanel
from pdesign.widgets.generic import RangeDataWidget

class FloatSpin(wx.Panel, RangeDataWidget):

	entry = None
	sb = None

	flag = True
	value = 0.0
	range_val = (0.0, 1.0)
	step = 0.01
	digits = 2
	callback = None

	def __init__(self, parent, value=0.0, range_val=(0.0, 1.0), step=0.01,
				digits=2, size=const.DEF_SIZE, width=0, spin_overlay=True,
				onchange=None, check_focus=True):

		self.callback = onchange
		if const.is_mac(): spin_overlay = False

		wx.Panel.__init__(self, parent)
		#self.SetBackgroundColour(wx.RED)
		if spin_overlay:
			if const.is_gtk():
				self.entry = Entry(self, '', size=size, width=width)#,
						#onchange=self._check_entry, onenter=self._entry_enter)
				size = (-1, self.entry.GetSize()[1])
				self.sb = SpinButton(self, size=size)
				w_pos = self.entry.GetSize()[0] - 5
				self.sb.SetPosition((w_pos, -1))
				line = HPanel(self)
				line.SetSize((1, self.sb.GetSize()[1] - 1))
				line.set_bg(const.UI_COLORS['dark_shadow'])
				line.SetPosition((w_pos - 1, -1))
			elif const.is_msw():
				self.entry = Entry(self, '', size=size, width=width)#,
						#onchange=self._check_entry, onenter=self._entry_enter)
				size = (-1, self.entry.GetSize()[1] - 1)
				self.sb = SpinButton(self.entry, size=size)
				w_pos = self.entry.GetSize()[0] - self.sb.GetSize()[0] - 2
				self.sb.SetPosition((w_pos, -2))
		else:
			self.box = wx.BoxSizer(const.HORIZONTAL)
			self.SetSizer(self.box)
			self.entry = Entry(self, '', size=size, width=width)#,
						#onchange=self._check_entry, onenter=self._entry_enter)
			self.box.Add(self.entry, 0, wx.ALL)
			size = (-1, self.entry.GetSize()[1])
			self.sb = SpinButton(self, size=size)#, onchange=self._check_spin)
			self.box.Add(self.sb, 0, wx.ALL)


class WidgetPanel(HPanel):

	name = 'Basic widgets'
	spin = None

	def __init__(self, parent):
		HPanel.__init__(self, parent)
		self.build()

	def build(self):
		flags = LEFT | CENTER
		pflags = ALL | EXPAND
		self.add(FloatSpin(self), 0, ALL, 2)
		self.add(FloatSpin(self), 0, ALL, 2)


app = Application('wxWidgets')
mw = MainWindow('Spin widget', (300, 250))
p = VPanel(mw)
mw.add(p, 1, ALL | EXPAND)
panel = WidgetPanel(mw)
p.add(panel, 1, ALL | EXPAND, 10)
app.mw = mw
app.run()
