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

from pdesign.resources import icons
from pdesign.widgets import const, HPanel

class AppStubPanel(HPanel):

	bmp = None
	bmp_size = ()

	def __init__(self, parent):
		HPanel.__init__(self, parent)
		self.set_bg(const.UI_COLORS['workspace'])
		self.bmp = wx.ArtProvider.GetBitmap(icons.CAIRO_BANNER, size=const.DEF_SIZE)
		self.bmp_size = self.bmp.GetSize()
		self.Bind(wx.EVT_PAINT, self._on_paint, self)
		self.Bind(wx.EVT_SIZE, self._on_resize, self)

	def hide(self):
		self.Hide()

	def refresh(self, x=0, y=0, w=0, h=0):
		if not w: w, h = self.GetSize()
		self.Refresh(rect=wx.Rect(x, y, w, h))

	def _on_resize(self, event):
		self.refresh()

	def _on_paint(self, event):
		h = self.GetSize()[1]
		pdc = wx.PaintDC(self.panel)
		try:
			dc = wx.GCDC(self.pdc)
		except:dc = pdc
		dc.BeginDrawing()

		x = 10
		y = h - self.bmp_size[1] - 10
		dc.DrawBitmap(self.bmp, x, y, True)

		if not pdc == dc:
			dc.EndDrawing()
			pdc.EndDrawing()
		else:
			dc.EndDrawing()
		pdc = dc = None


