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

from pdesign import _, events
from pdesign.resources import icons, get_bmp
from pdesign.widgets import LEFT, CENTER, FloatSpin, Slider
from generic import CtxPlugin

class RectanglePlugin(CtxPlugin):

	name = 'RectanglePlugin'
	corners = [0, 0, 0, 0]
	update_flag = False

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)
		events.connect(events.DOC_CHANGED, self.update)
		events.connect(events.SELECTION_CHANGED, self.update)

	def build(self):
		bmp = get_bmp(self, icons.CTX_ROUNDED_RECT, _('Rounded rectangle'))
		self.add(bmp, 0, LEFT | CENTER, 2)

		self.slider = Slider(self, 0, (0, 100), onchange=self.slider_changes)
		self.add(self.slider, 0, LEFT | CENTER, 2)

		self.num_spin = FloatSpin(self, 0, (0.0, 100.0), 1.0, 0,
							width=3, onchange=self.changes)
		self.add(self.num_spin, 0, LEFT | CENTER, 2)

	def slider_changes(self, *args):
		if self.update_flag: return
		self.apply_changes(self.slider.get_value() / 100.0)

	def changes(self, *args):
		if self.update_flag: return
		self.apply_changes(self.num_spin.get_value() / 100.0)

	def apply_changes(self, val):
		if self.insp.is_selection():
			selection = self.app.current_doc.selection
			if self.insp.is_obj_rect(selection.objs[0]):
				if not val == self.corners[0]:
					corners = [val, val, val, val]
					self.app.current_doc.api.set_rect_corners(corners)

	def update(self, *args):
		if self.insp.is_selection():
			selection = self.app.current_doc.selection
			if self.insp.is_obj_rect(selection.objs[0]):
				self.update_flag = True
				self.corners = [] + selection.objs[0].corners
				self.slider.set_value(int(self.corners[0] * 100))
				self.num_spin.set_value(self.corners[0] * 100.0)
				self.update_flag = False
