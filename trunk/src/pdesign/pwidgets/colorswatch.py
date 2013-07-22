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

from pdesign.widgets import HPanel

class ColorSwatch(HPanel):

	color = (255, 0, 0)

	def __init__(self, parent, size=(35, 16)):
		HPanel.__init__(self, parent)
		self.add(size)
		self.Bind(wx.EVT_PAINT, self._on_paint, self)

	def _on_paint(self, event):
		w, h = self.GetSize()
		pdc = wx.PaintDC(self.panel)
		try:
			dc = wx.GCDC(self.pdc)
		except:dc = pdc
		dc.BeginDrawing()

		pdc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
		pdc.SetBrush(wx.Brush(wx.Colour(*self.color)))
		pdc.DrawRectangle(0, 0, w, h)

		if not pdc == dc:
			dc.EndDrawing()
			pdc.EndDrawing()
		else:
			dc.EndDrawing()
		pdc = dc = None

