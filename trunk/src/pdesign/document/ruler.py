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

import os, math
import wx
import cairo

from uc2 import uc2const
from uc2.formats.pdxf.const import DOC_ORIGIN_CENTER, DOC_ORIGIN_LL, DOC_ORIGIN_LU

from pdesign import config
from pdesign.resources import get_icon, icons
from pdesign.widgets.const import HORIZONTAL
from pdesign.widgets import HPanel
from pdesign.widgets import copy_surface_to_bitmap

HFONT = {}
VFONT = {}
fntdir = os.path.join(config.resource_dir, 'fonts', 'ruler-font')
for char in '.,-0123456789':
	if char in '.,': file_name = os.path.join(fntdir, 'hdot.png')
	else: file_name = os.path.join(fntdir, 'h%s.png' % char)
	surface = cairo.ImageSurface.create_from_png(file_name)
	HFONT[char] = (surface.get_width(), surface)

	if char in '.,': file_name = os.path.join(fntdir, 'vdot.png')
	else: file_name = os.path.join(fntdir, 'v%s.png' % char)
	surface = cairo.ImageSurface.create_from_png(file_name)
	VFONT[char] = (surface.get_height(), surface)

CAIRO_WHITE = [1.0, 1.0, 1.0]
CAIRO_BLACK = [0.0, 0.0, 0.0]

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

	presenter = None
	eventloop = None
	style = None

	init_flag = False
	surface = None
	ctx = None
	width = 0
	height = 0

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
		canvas = self.presenter.canvas
		pw, ph = self.presenter.get_page_size()
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

			coef = round(50.0 / dx)
			if not coef:coef = 1.0
			dxt = dx * coef
			sxt = (x0 / dxt - math.floor(x0 / dxt)) * dxt

			i = -1
			pos = 0
			while pos < w:
				pos = sxt + i * dxt
				doc_pos = canvas.point_win_to_doc((pos, 0))[0] + pw / 2.0
				doc_pos *= uc2const.point_dict[config.default_unit]
				txt = str(int(round(doc_pos)))
				text_ticks.append((sxt + i * dxt, txt))
				i += 1

		else:
			i = -1
			pos = 0
			while pos < h:
				pos = sy + i * dy
				small_ticks.append(sy + i * dy)
				if dy > 10:small_ticks.append(pos + dy * .5)
				i += 1

			coef = round(50.0 / dy)
			if not coef:coef = 1.0
			dyt = dy * coef
			syt = (y0 / dyt - math.floor(y0 / dyt)) * dyt

			i = -1
			pos = 0
			while pos < h:
				pos = syt + i * dyt
				doc_pos = canvas.point_win_to_doc((0, pos))[1] + ph / 2.0
				doc_pos *= uc2const.point_dict[config.default_unit]
				txt = str(int(round(doc_pos)))
				text_ticks.append((syt + i * dyt, txt))
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
		if self.surface is None:
			self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
			self.width = w
			self.height = h
		elif self.width <> w or self.height <> h:
			self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
			self.width = w
			self.height = h
		self.ctx = cairo.Context(self.surface)
		self.ctx.set_matrix(cairo.Matrix(1.0, 0.0, 0.0, 1.0, 0.0, 0.0))
		self.ctx.set_source_rgb(*CAIRO_WHITE)
		self.ctx.paint()
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.set_line_width(1.0)
		self.ctx.set_dash([])
		self.ctx.set_source_rgba(*CAIRO_BLACK)
		if self.init_flag:
			if self.style == HORIZONTAL: self.hrender(w, h)
			else: self.vrender(w, h)
		pdc.DrawBitmap(copy_surface_to_bitmap(self.surface), 0, 0, True)

	def hrender(self, w, h):
		self.ctx.move_to(0, h)
		self.ctx.line_to(w, h)

		small_ticks, text_ticks = self.get_ticks()
		for item in small_ticks:
			self.ctx.move_to(item, h - 5)
			self.ctx.line_to(item, h - 1)

		for pos, txt in text_ticks:
			self.ctx.move_to(pos, h - 10)
			self.ctx.line_to(pos, h - 1)

		self.ctx.stroke()

		for pos, txt in text_ticks:
			for character in txt:
				data = HFONT[character]
				self.ctx.set_source_surface(data[1], int(pos), 3)
				self.ctx.paint()
				pos += data[0]

	def vrender(self, w, h):
		self.ctx.move_to(w, 0)
		self.ctx.line_to(w, h)

		small_ticks, text_ticks = self.get_ticks()
		for item in small_ticks:
			self.ctx.move_to(w - 5, item)
			self.ctx.line_to(w - 1, item)

		for item, txt in text_ticks:
			self.ctx.move_to(w - 10, item)
			self.ctx.line_to(w - 1, item)

		self.ctx.stroke()

		for pos, txt in text_ticks:
			for character in txt:
				data = VFONT[character]
				self.ctx.set_source_surface(data[1], 3, int(pos) - data[0])
				self.ctx.paint()
				pos -= data[0]
