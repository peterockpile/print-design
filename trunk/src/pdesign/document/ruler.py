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

from uc2.formats.pdxf.const import DOC_ORIGIN_CENTER, DOC_ORIGIN_LL, DOC_ORIGIN_LU

from pdesign import config
from pdesign.resources import get_icon, icons
from pdesign.widgets.const import HORIZONTAL
from pdesign.widgets import HPanel

class RulerCorner(HPanel):

	bitmaps = {}
	presenter = None
	origin = DOC_ORIGIN_LL

	def __init__(self, presenter, parent):
		self.presenter = presenter
		HPanel.__init__(self, parent)
		size = config.ruler_size
		if not self.bitmaps:
			self.bitmaps[DOC_ORIGIN_CENTER] = get_icon(icons.ORIGIN_CENTER)
			self.bitmaps[DOC_ORIGIN_LL] = get_icon(icons.ORIGIN_LL)
			self.bitmaps[DOC_ORIGIN_LU] = get_icon(icons.ORIGIN_LU)
		self.add((size, size))
		self.SetBackgroundColour(wx.WHITE)
		self.Bind(wx.EVT_PAINT, self._on_paint, self)

	def destroy(self):
		self.presenter = None

	def refresh(self, x=0, y=0, w=0, h=0):
		if not w: w, h = self.GetSize()
		self.Refresh(rect=wx.Rect(x, y, w, h))

	def _on_paint(self, event):
		w, h = self.panel.GetSize()
		pdc = wx.PaintDC(self.panel)
		try:dc = wx.GCDC(pdc)
		except:dc = pdc
		pdc.BeginDrawing()
		dc.BeginDrawing()
		grad_start = wx.Colour(0, 0, 0, 255)
		grad_end = wx.Colour(0, 0, 0, 0)
		rect = wx.Rect(0, h - 1, w * 2, 1)
		dc.GradientFillLinear(rect, grad_start, grad_end, nDirection=wx.WEST)
		rect = wx.Rect(w - 1, 0, 1, h * 2)
		dc.GradientFillLinear(rect, grad_start, grad_end, nDirection=wx.NORTH)
		bmp = self.bitmaps[self.origin]
		dc.DrawBitmap(bmp, 1, 1, False)

class Ruler(HPanel):

	def __init__(self, presenter, parent, style=HORIZONTAL):
		self.presenter = presenter
		self.style = style
		HPanel.__init__(self, parent)
		size = config.ruler_size
		self.add((size, size))
		self.SetBackgroundColour(wx.WHITE)
		self.Bind(wx.EVT_PAINT, self._on_paint, self)

	def destroy(self):
		self.presenter = None

	def refresh(self, x=0, y=0, w=0, h=0):
		if not w: w, h = self.GetSize()
		self.Refresh(rect=wx.Rect(x, y, w, h))

	def _on_paint(self, event):
		w, h = self.panel.GetSize()
		pdc = wx.PaintDC(self.panel)
		pdc.BeginDrawing()
		black = wx.BLACK
		pdc.SetBrush(wx.TRANSPARENT_BRUSH)
		pdc.SetPen(wx.Pen(black, 1))

		if self.style == HORIZONTAL:
			pdc.DrawLine(0, h - 1, w, h - 1)
		else:
			pdc.DrawLine(w - 1, 0, w - 1, h)
