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

	def __init__(self, parent):
		VPanel.__init__(self, parent)
		self.Bind(wx.EVT_PAINT, self.on_paint)
		self.Bind(wx.EVT_LEFT_DOWN, self.mouse_down)
		self.Bind(wx.EVT_LEFT_UP, self.mouse_up)
		self.Bind(wx.EVT_MOTION, self.mouse_move)

	def mouse_down(self, event):
		self.drawing = True
		self.start = list(event.GetPositionTuple())
		self.end = list(event.GetPositionTuple())
		print 'down'

	def mouse_up(self, event):
		self.render_frame()
		self.drawing = False
		self.start = self.end = []
		print 'up'

	def mouse_move(self, event):
		if self.drawing:
			self.render_frame()
			self.end = list(event.GetPositionTuple())
			self.render_frame()

	def render_frame(self):
		if self.start and self.end:
			x, y = self.start
			x1, y1 = self.end
			dc = wx.ClientDC(self)
			dc.SetLogicalFunction(wx.INVERT)
			pen = wx.Pen(wx.Colour(0, 0, 0), 1)
			#pen.SetDashes([5, 5, 5, 5])
			dc.SetPen(pen)
			dc.SetBrush(wx.TRANSPARENT_BRUSH)
			dc.DrawRectangle(x, y, x1 - x, y1 - y)

	def on_paint(self, event):
		dc = wx.BufferedPaintDC(self)
		width, height = dc.GetSize()
		surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
		ctx = cairo.Context(surface)
		ctx.set_source_rgb(1, 1, 1)
		ctx.paint()
		ctx.set_line_width(15)
		ctx.move_to(125, 25)
		ctx.line_to(225, 225)
		ctx.rel_line_to(-200, 0)
		ctx.close_path()
		ctx.set_source_rgba(0, 0, 0.5, 1)
		ctx.stroke()
		dc.DrawBitmap(copy_surface_to_bitmap(surface), 0, 0, True)

app = Application('Cairo test')
mw = MainWindow(app.app_name, (700, 500))
p = CairoCanvas(mw)
mw.add(p, 1, ALL | EXPAND)
app.mw = mw
app.run()
