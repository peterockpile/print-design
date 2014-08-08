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

import wx, time

from uc2 import uc2_init
from uc2.formats import get_loader

from pdesign.widgets import const, BOTTOM, CENTER, LEFT, ALL, EXPAND
from pdesign.widgets import Application, MainWindow, Button
from pdesign.widgets import HPanel, VPanel
from pdesign.widgets.basic import SpinButton, SizedPanel
from pdesign.widgets.generic import RangeDataWidget
import gc

class WidgetPanel(HPanel):

	uc_app = None
	docs = []
	doc = None

	def __init__(self, parent):
		HPanel.__init__(self, parent)
		self.build()
		self.uc_app = uc2_init()

	def build(self):
		flags = CENTER
		self.add(Button(self, 'Load', onclick=self.load), 0, flags, 5)
		self.add(Button(self, 'Release', onclick=self.release), 0, flags, 5)
		self.add(Button(self, 'GC', onclick=self.collect), 0, flags, 5)

	def load(self, *args):
		filepath = 'data/sample.pdxf'
		filepath2 = 'data/sample2.pdxf'
		loader = get_loader(filepath)
		i = 0
		while i < 20:
			self.docs.append(loader(self.uc_app.appdata, filepath2))
			self.release()
			self.docs.append(loader(self.uc_app.appdata, filepath))
			self.release()
			self.docs.append(loader(self.uc_app.appdata, filepath2))
			self.release()
			self.docs.append(loader(self.uc_app.appdata, filepath))
			self.release()
			#time.sleep(1)
			i += 1

	def release(self, *args):
		for doc in self.docs:
			doc.close()
			self.docs.remove(doc)
#			gc.collect()
		self.docs = []

	def collect(self, *args):
		print 'GC:', gc.collect()


app = Application('wxWidgets')
mw = MainWindow('Memory leak test', (300, 100))
p = VPanel(mw)
mw.add(p, 1, ALL | EXPAND)
panel = WidgetPanel(mw)
p.add(panel, 1, ALL | EXPAND, 10)
app.mw = mw
app.run()
