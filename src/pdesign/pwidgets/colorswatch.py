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

from uc2 import uc2const
from uc2.cms import verbose_color
from uc2.uc2const import point_dict
from uc2.formats.pdxf.const import FILL_SOLID

from pdesign import _, config
from pdesign.widgets import HPanel

class ColorSwatch(HPanel):

	rgb_color = (255, 0, 0)

	def __init__(self, parent, size=(35, 16)):
		HPanel.__init__(self, parent)
		self.add(size)
		self.Bind(wx.EVT_PAINT, self._on_paint, self)

	def refresh(self, x=0, y=0, w=0, h=0):
		if not w: w, h = self.GetSize()
		self.Refresh(rect=wx.Rect(x, y, w, h))

	def _on_paint(self, event):
		w, h = self.GetSize()
		pdc = wx.PaintDC(self.panel)
		try:
			dc = wx.GCDC(self.pdc)
		except:dc = pdc
		dc.BeginDrawing()

		pdc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
		if self.rgb_color:
			pdc.SetBrush(wx.Brush(wx.Colour(*self.rgb_color)))
		else:
			pdc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))

		pdc.DrawRectangle(0, 0, w, h)

		if not self.rgb_color:
			dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
			dc.DrawLine(0, 0, w, h - 1)
			dc.DrawLine(0, h - 1, w, 0)

		if not pdc == dc:
			dc.EndDrawing()
			pdc.EndDrawing()
		else:
			dc.EndDrawing()
		pdc = dc = None

class FillSwatch(ColorSwatch):

	non_solid = False
	colorspace = ''
	color = []
	alpha = 1.0
	color_name = ''


	def __init__(self, parent, app, label, size=(35, 16)):
		self.app = app
		self.label = label
		ColorSwatch.__init__(self, parent, size)

	def update_from_obj(self, obj):
		fill = obj.style[0]
		if fill:
			if fill[1] == FILL_SOLID:
				self.non_solid = False
				self.colorspace = fill[2][0]
				self.color = [] + fill[2][1]
				self.alpha = fill[2][2]
				self.color_name = '' + fill[2][3]
			else:
				self.non_solid = True
				self.color = []
		else:
			self.colorspace = None
			self.color = []
			self.alpha = 1.0
			self.color_name = ''
			self.non_solid = False

		if self.color:
			cms = self.app.current_doc.cms
			r, g, b = cms.get_display_color(fill[2])
			self.rgb_color = (int(r * 255), int(g * 255), int(b * 255))
			self.update_label(fill[2])
		else:
			self.rgb_color = ()
			self.update_label()
		self.refresh()

	def update_label(self, color=[]):
		text = _('Fill:')
		if self.non_solid:
			pass
		elif self.colorspace is None:
			text += ' ' + _('None')
		else:
			text += ' ' + verbose_color(color)
		self.label.set_text(text)

class StrokeSwatch(ColorSwatch):

	point_val = 0

	def __init__(self, parent, app, label, size=(35, 16)):
		self.app = app
		self.label = label
		ColorSwatch.__init__(self, parent, size)

	def update_from_obj(self, obj):
		stroke = obj.style[1]
		if stroke:
			self.point_val = stroke[1]
			cms = self.app.current_doc.cms
			r, g, b = cms.get_display_color(stroke[2])
			self.rgb_color = (int(r * 255), int(g * 255), int(b * 255))
		else:
			self.point_val = 0
			self.rgb_color = ()
		self.update_val()
		self.refresh()

	def update_val(self):
		text = _('Stroke:')
		if self.point_val:
			unit = self.app.current_doc.model.doc_units
			val = str(round(self.point_val * point_dict[unit], 3))
			text += (' %s ') % (val)
			text += uc2const.unit_short_names[unit]
		else:
			text += ' ' + _('None')
		self.label.set_text(text)
