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

import math
import wx

from uc2 import uc2const
from uc2.uc2const import point_dict, unit_dict

from pdesign import _, events
from pdesign.widgets import Label, FloatSpin
from pdesign.resources import icons, get_icon

class UnitLabel(Label):

	app = None
	insp = None
	units = uc2const.UNIT_MM

	def __init__(self, app, parent):
		self.app = app
		self.insp = app.insp
		if self.insp.is_doc(): self.units = app.current_doc.model.doc_units
		text = uc2const.unit_short_names[self.units]
		Label.__init__(self, parent, text)
		events.connect(events.DOC_CHANGED, self.update)
		events.connect(events.DOC_MODIFIED, self.update)

	def update(self, *args):
		if not self.insp.is_doc(): return
		if self.units == self.app.current_doc.model.doc_units: return
		self.units = self.app.current_doc.model.doc_units
		text = uc2const.unit_short_names[self.units]
		self.set_text(text)

class UnitSpin(FloatSpin):

	app = None
	insp = None
	ucallback = None
	point_value = 0.0
	units = uc2const.UNIT_MM

	def __init__(self, app, parent, val=0.0, onchange=None):
		self.app = app
		self.insp = app.insp
		self.point_value = val
		self.ucallback = onchange
		if self.insp.is_doc(): self.units = app.current_doc.model.doc_units
		val = self.point_value * point_dict[self.units]
		FloatSpin.__init__(self, parent, val, (0.0, 100000.0),
						step=1.0, width=5,
						onchange=self.update_point_value)
		events.connect(events.DOC_MODIFIED, self.update_units)

	def update_point_value(self, *args):
		self.point_value = self.get_value() * unit_dict[self.units]
		if not self.ucallback is None: self.ucallback()

	def get_point_value(self):
		return self.point_value

	def set_point_value(self, val):
		if not self.point_value == val:
			self.point_value = val
			self.set_value(self.point_value * point_dict[self.units])

	def update_units(self, *args):
		if not self.insp.is_doc(): return
		if self.units == self.app.current_doc.model.doc_units: return
		self.units = self.app.current_doc.model.doc_units
		self.set_value(self.point_value * point_dict[self.units])

class RatioToggle(wx.StaticBitmap):

	state = True
	ratio = None
	no_ratio = None
	onchange = None

	def __init__(self, parent, state=True, onchange=None):
		self.onchange = onchange
		self.ratio = get_icon(icons.CTX_RATIO)
		self.no_ratio = get_icon(icons.CTX_NO_RATIO)
		wx.StaticBitmap.__init__(self, parent, -1, self.ratio)
		self.set_active(state)
		self.Bind(wx.EVT_LEFT_UP, self.change, self)

	def change(self, *args):
		self.set_active(not self.state)
		if not self.onchange is None: self.onchange()

	def get_active(self):
		return self.state

	def set_active(self, state):
		self.state = state
		bmp = self.no_ratio
		tooltip = _("Don't keep ratio")
		if self.state:
			bmp = self.ratio
			tooltip = _("Keep ratio")
		self.SetBitmap(bmp)
		self.SetToolTipString(tooltip)

class AngleSpin(FloatSpin):

	ucallback = None
	angle_value = 0.0

	def __init__(self, parent, val=0.0, onchange=None):
		self.angle_value = val
		self.ucallback = onchange
		FloatSpin.__init__(self, parent, val, (-360.0, 360.0),
						step=1.0, width=5,
						onchange=self.update_angle_value,
						check_focus=False)

	def update_angle_value(self, *args):
		self.angle_value = self.get_value() * math.pi / 180.0
		if not self.ucallback is None: self.ucallback()

	def get_angle_value(self):
		return self.angle_value

	def set_angle_value(self, val):
		if not self.angle_value == val:
			self.angle_value = val
			self.set_value(round(self.angle_value * 180 / math.pi, 2))
