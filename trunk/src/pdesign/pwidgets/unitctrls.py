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

from uc2 import uc2const
from uc2.uc2const import point_dict, unit_dict

from pdesign import events
from pdesign.widgets import const, Label, FloatSpin

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
	update_flag = False

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

