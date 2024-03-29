# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2013 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import wx

from pdesign import _
from pdesign.widgets import const, HPanel, ImageButton, ImageLabel
from pdesign.pwidgets import HPalette
from pdesign.resources import CMYK_PALETTE, icons

class AppPalettePanel(HPanel):

	left_but = None
	dleft_but = None
	no_color = None
	palette = None
	right_but = None
	dright_but = None

	def __init__(self, mw):
		self.app = mw.app
		self.mw = mw
		HPanel.__init__(self, mw, const.TOP)
		self.add((1, 20))

		self.palette = HPalette(self.panel, self.app.default_cms, CMYK_PALETTE,
							onleftclick=self.app.proxy.fill_selected,
							onrightclick=self.app.proxy.stroke_selected,
							onmin=self.left_enable,
							onmax=self.right_enable)

		native = False
		if const.is_gtk(): native = True

		tip = _('Scroll palette to left')
		self.dleft_but = ImageButton(self.panel, icons.DOUBLE_ARROW_LEFT,
								tooltip=tip, decoration_padding=4, native=native,
								onclick=self.palette.dscroll_left, repeat=True)
		self.add(self.dleft_but)
		self.left_but = ImageButton(self.panel, icons.ARROW_LEFT, tooltip=tip,
								decoration_padding=4, native=native,
								onclick=self.palette.scroll_left, repeat=True)
		self.add(self.left_but)

		tip = _('Empty pattern')
		self.no_color = ImageLabel(self.panel, icons.NO_COLOR, tooltip=tip,
								 onclick=self.set_no_fill)
		self.no_color.Bind(wx.EVT_RIGHT_UP, self.set_no_stroke, self.no_color)
		self.add(self.no_color)

		self.add(self.palette, 1, const.ALL | const.EXPAND, 1)

		tip = _('Scroll palette to right')
		self.right_but = ImageButton(self.panel, icons.ARROW_RIGHT, tooltip=tip,
								decoration_padding=4, native=native,
								onclick=self.palette.scroll_right, repeat=True)
		self.add(self.right_but)
		self.dright_but = ImageButton(self.panel, icons.DOUBLE_ARROW_RIGHT,
								tooltip=tip, decoration_padding=4, native=native,
								onclick=self.palette.dscroll_right, repeat=True)
		self.add(self.dright_but)
		self.left_enable(False)


	def set_no_fill(self): self.app.proxy.fill_selected([])
	def set_no_stroke(self, event): self.app.proxy.stroke_selected([])

	def set_fill(self, color):
		print color

	def set_stroke(self, color):
		print color

	def left_enable(self, value):
		if not value == self.left_but.get_enabled():
			self.left_but.set_enable(value)
			self.dleft_but.set_enable(value)

	def right_enable(self, value):
		if not value == self.right_but.get_enabled():
			self.right_but.set_enable(value)
			self.dright_but.set_enable(value)
