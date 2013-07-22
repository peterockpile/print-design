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

from pdesign import events
from pdesign.widgets import const, TOP, LEFT, CENTER, HPanel, Label
from pdesign.pwidgets import ColorSwatch

class AppStatusbar(HPanel):

	mw = None
	panel1 = None
	info = None
	panel2 = None
	clr_monitor = None

	def __init__(self, mw):
		self.mw = mw
		HPanel.__init__(self, mw, border=TOP)
		self.add((1, 20))
		panel1 = HPanel(self.panel)
		panel1.add((5, 20))
		self.info = Label(panel1.panel, text='')
		panel1.add(self.info, 0, LEFT | CENTER)
		self.add(panel1, 1, const.ALL | const.EXPAND)
		self.clr_monitor = ColorMonitor(self.mw.app, self.panel)
		self.add(self.clr_monitor, 0, const.ALL | const.EXPAND)
		self.clr_monitor.hide()
		events.connect(events.APP_STATUS, self._on_event)

	def _on_event(self, *args):
		self.info.set_text(args[0])
		self.Layout()

class ColorMonitor(HPanel):

	fill_txt = None
	fill_swatch = None
	stroke_txt = None
	stroke_swatch = None

	def __init__(self, app, parent):
		self.app = app
		HPanel.__init__(self, parent)
		self.fill_txt = Label(self.panel, text='Fill:')
		self.add(self.fill_txt, 0, LEFT | CENTER)
		self.fill_swatch = ColorSwatch(self.panel)
		self.add(self.fill_swatch, 0, LEFT | CENTER, 2)
		self.stroke_txt = Label(self.panel, text='Stroke:')
		self.add(self.stroke_txt, 0, LEFT | CENTER, 10)
		self.stroke_swatch = ColorSwatch(self.panel)
		self.add(self.stroke_swatch, 0, LEFT | CENTER, 2)
		self.add((5, 5))




