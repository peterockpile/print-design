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

from pdesign import _, config, events
from pdesign.resources import icons, get_bmp
from pdesign.widgets import const, LEFT, CENTER, Label
from pdesign.pwidgets import UnitSpin, RatioToggle
from generic import CtxPlugin

class ResizePlugin(CtxPlugin):

	name = 'ResizePlugin'
	update_flag = False

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)

	def build(self):
		bmp = get_bmp(self, icons.CTX_OBJECT_RESIZE, _('Object size'))
		self.add(bmp, 0, LEFT | CENTER, 2)

		self.width_spin = UnitSpin(self.app, self,
							onchange=self.width_spin_changed)
		self.add(self.width_spin, 0, LEFT | CENTER, 2)

		self.add(get_bmp(self, icons.CTX_W_ON_H), 0, LEFT | CENTER, 1)

		self.height_spin = UnitSpin(self.app, self,
							onchange=self.height_spin_changed)
		self.add(self.height_spin, 0, LEFT | CENTER, 2)

		self.keep_ratio = RatioToggle(self)
		self.add(self.keep_ratio, 0, LEFT | CENTER, 2)

	def width_spin_changed(self, *args):pass
	def height_spin_changed(self, *args):pass
