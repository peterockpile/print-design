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
import cairo

from pdesign.widgets import const, copy_surface_to_bitmap
from pdesign.widgets import BOTTOM, CENTER, LEFT, ALL, EXPAND, TOP
from pdesign.widgets import Application, MainWindow, VPanel, HPanel, Button, Label

class CairoCanvas(VPanel):

	drawing = False
	start = []
	end = []
	new_end = []
	surface = None
	temp_surface = None

	def __init__(self, parent):
		VPanel.__init__(self, parent)
		self.Bind(wx.EVT_PAINT, self.on_paint)
		self.Bind(wx.EVT_LEFT_DOWN, self.mouse_down)
		self.Bind(wx.EVT_LEFT_UP, self.mouse_up)
		self.Bind(wx.EVT_MOTION, self.mouse_move)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_timer)

	def mouse_down(self, event):
		self.drawing = True
		self.start = list(event.GetPositionTuple())
		self.end = list(event.GetPositionTuple())
		self.timer.Start(50)
		print 'down'

	def mouse_up(self, event):
		self.timer.Stop()
		self.clear_frame()
		self.drawing = False
		self.start = self.end = self.new_end = []
		print 'up'

	def mouse_move(self, event):
		if self.drawing:
			self.new_end = list(event.GetPositionTuple())

	def on_timer(self, event):
		if not self.drawing: return
		if self.start and self.end:
			if self.new_end:
				self.clear_frame()
				self.end = self.new_end
				self.new_end = []
				self.render_frame()

	def norm_rect(self, start, end):
		x0, y0 = self.start
		x1, y1 = self.end
		x_min = min(x0, x1)
		x_max = max(x0, x1)
		y_min = min(y0, y1)
		y_max = max(y0, y1)
		w = x_max - x_min
		h = y_max - y_min
		return [x_min, y_min, w, h]

	def render_frame(self):
		if self.start and self.end:
			x, y, w, h = self.norm_rect(self.start, self.end)
			if not w: w = 1
			if not h: h = 1
			temp_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
			ctx = cairo.Context(temp_surface)
#			ctx.set_source_surface(self.surface, -x, -y)
#			ctx.paint()
			ctx.set_antialias(cairo.ANTIALIAS_NONE)
			ctx.set_line_width(1.0)
			ctx.set_source_rgb(1, 1, 1)
			ctx.rectangle(1, 1, w - 1, h - 1)
			ctx.stroke()
			ctx.set_dash([5, 5])
			ctx.set_source_rgb(0, 0, 0)
			ctx.rectangle(1, 1, w - 1, h - 1)
			ctx.stroke()
			dc = wx.ClientDC(self)
#			dc.DrawBitmap(copy_surface_to_bitmap(temp_surface), x, y)
			rects = [[0, 0, 1, h - 1], [0, 0, w - 1, 1],
				[w - 1, 0, 1, h - 1], [0, h - 1, w - 1, 1]]
			for rect in rects:
				x0, y0, w, h = rect
				if not w: w = 1
				if not h: h = 1
				surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
				ctx = cairo.Context(surface)
				ctx.set_source_surface(temp_surface, -x0, -y0)
				ctx.paint()
				dc.DrawBitmap(copy_surface_to_bitmap(surface), x0 + x, y0 + y)

	def clear_frame(self):
		if self.start and self.end:
			x, y, w, h = self.norm_rect(self.start, self.end)
			dc = wx.ClientDC(self)
			rects = [[x, y, 1, h], [x, y, w, 1],
					[x + w - 1, y, 1, h], [x, y + h - 1, w, 1]]
			for rect in rects:
				x0, y0, w, h = rect
				if not w: w = 1
				if not h: h = 1
				surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
				ctx = cairo.Context(surface)
				ctx.set_source_surface(self.surface, -x0, -y0)
				ctx.paint()
				dc.DrawBitmap(copy_surface_to_bitmap(surface), x0, y0)

	def on_paint(self, event):
		dc = wx.PaintDC(self)
		self.draw_content(*dc.GetSize())
		dc.DrawBitmap(copy_surface_to_bitmap(self.surface), 0, 0)

	def draw_content(self, width, height):
		self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
		ctx = cairo.Context(self.surface)
		ctx.set_source_rgb(1, 1, 1)
		ctx.paint()
		ctx.set_line_width(15)
		ctx.move_to(125, 25)
		ctx.line_to(225, 225)
		ctx.rel_line_to(-200, 0)
		ctx.close_path()
		ctx.set_source_rgba(0, 0, 0.5, 1)
		ctx.stroke()

app = Application('Cairo test')
mw = MainWindow(app.app_name, (700, 500))
p = CairoCanvas(mw)
mw.add(p, 1, ALL | EXPAND)
app.mw = mw
app.run()
