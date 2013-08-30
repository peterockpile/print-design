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

from uc2.uc2const import PAGE_FORMATS, PAGE_FORMAT_NAMES, PORTRAIT, LANDSCAPE

from pdesign import _, events
from pdesign.widgets import Combolist, LEFT, CENTER
from generic import CtxPlugin


class PagePlugin(CtxPlugin):

	name = 'PagePlugin'

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)

	def build(self):
		self.formats = PAGE_FORMAT_NAMES + [_('Custom'), ]
		self.combo = Combolist(self, items=self.formats)
		self.add(self.combo, 0, LEFT | CENTER)
