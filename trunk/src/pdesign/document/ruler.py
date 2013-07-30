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

import math
import wx

from uc2 import uc2const
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
		dc.DrawBitmap(bmp, 1, 1, True)

class Ruler(HPanel):

	init_flag = False

	def __init__(self, presenter, parent, style=HORIZONTAL):
		self.presenter = presenter
		self.eventloop = presenter.eventloop
		self.style = style
		HPanel.__init__(self, parent)
		size = config.ruler_size
		self.add((size, size))
		self.SetBackgroundColour(wx.WHITE)
		self.Bind(wx.EVT_PAINT, self._on_paint, self)
		self.eventloop.connect(self.eventloop.VIEW_CHANGED, self.repaint)

	def destroy(self):
		self.presenter = None

	def calc_ruler(self):
		canvas = self.presenter.canvas
		w, h = self.presenter.get_page_size()
		x = y = 0
		dx = dy = uc2const.unit_dict[config.default_unit]
		origin = self.presenter.model.doc_origin
		if origin == DOC_ORIGIN_LL:
			x0, y0 = canvas.point_doc_to_win([-w / 2.0 + x, -h / 2.0 + y])
		elif origin == DOC_ORIGIN_LU:
			x0, y0 = canvas.point_doc_to_win([-w / 2.0 + x, h / 2.0 + y])
		else:
			x0, y0 = canvas.point_doc_to_win([x, y])
		dx = dx * canvas.zoom
		dy = dy * canvas.zoom
		sdist = config.snap_distance

		i = 0.0
		while dx < sdist + 3:
			i = i + 0.5
			dx = dx * 10.0 * i
		if dx / 2.0 > sdist + 3:
			dx = dx / 2.0

		i = 0.0
		while dy < sdist + 3:
			i = i + 0.5
			dy = dy * 10.0 * i
		if dy / 2.0 > sdist + 3:
			dy = dy / 2.0

		sx = (x0 / dx - math.floor(x0 / dx)) * dx
		sy = (y0 / dy - math.floor(y0 / dy)) * dy
		return (x0, y0, dx, dy, sx, sy)

	def get_ticks(self):
		w, h = self.panel.GetSize()
		x0, y0, dx, dy, sx, sy = self.calc_ruler()
		small_ticks = []
		text_ticks = []
		if self.style == HORIZONTAL:
			i = -1
			pos = 0
			while pos < w:
				pos = sx + i * dx
				small_ticks.append(sx + i * dx)
				if dx > 10:small_ticks.append(pos + dx * .5)
				i += 1

			coef = round(30.0 / dx)
			if not coef:coef = 1.0
			dxt = dx * coef
			sxt = (x0 / dxt - math.floor(x0 / dxt)) * dxt

			i = -1
			pos = 0
			while pos < w:
				pos = sxt + i * dxt
				text_ticks.append(sxt + i * dxt)
				i += 1

		else:
			i = -1
			pos = 0
			while pos < h:
				pos = sy + i * dy
				small_ticks.append(sy + i * dy)
				if dy > 10:small_ticks.append(pos + dy * .5)
				i += 1

			coef = round(30.0 / dy)
			if not coef:coef = 1.0
			dyt = dy * coef
			syt = (y0 / dyt - math.floor(y0 / dyt)) * dyt

			i = -1
			pos = 0
			while pos < h:
				pos = syt + i * dyt
				text_ticks.append(syt + i * dyt)
				i += 1

		return small_ticks, text_ticks

	def repaint(self, *args):
		self.init_flag = True
		self.refresh()

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

		if self.init_flag:
			ticks, text = self.get_ticks()
			if self.style == HORIZONTAL:
				for item in ticks: pdc.DrawLine(item, h - 5, item, h - 1)
				for item in text: pdc.DrawLine(item, h - 10, item, h - 1)
			else:
				for item in ticks: pdc.DrawLine(w - 5, item, w - 1, item)
				for item in text: pdc.DrawLine(w - 10, item, w - 1, item)


